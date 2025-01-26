from django import template
from django.utils.safestring import mark_safe
from core.models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def render_menu(context):
    user = context['request'].user
    menu_items = MenuItem.objects.filter(parent=None).order_by('order')
    
    def render_menu_item(item):
        if not item.groups.exists() or user.groups.filter(id__in=item.groups.all()).exists():
            children = item.children.all().order_by('order')
            child_html = ''.join([render_menu_item(child) for child in children])
            
            if child_html:
                return f'''
                    <div class="menu-item">
                        <button class="flex items-center w-full text-left py-2 px-4 hover:bg-gray-700 focus:outline-none">
                            <span>{item.name}</span>
                            <svg class="ml-auto h-4 w-4 transform transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>
                        <div class="pl-4 hidden">{child_html}</div>
                    </div>
                '''
            else:
                return f'<a href="{item.url}" class="block py-2 px-4 hover:bg-gray-700">{item.name}</a>'
        return ''

    menu_html = ''.join([render_menu_item(item) for item in menu_items])
    return mark_safe(f'''
        <div class="menu">
            {menu_html}
        </div>
        <script>
            document.querySelectorAll('.menu-item > button').forEach(button => {{
                button.addEventListener('click', () => {{
                    const submenu = button.nextElementSibling;
                    submenu.classList.toggle('hidden');
                    button.querySelector('svg').classList.toggle('rotate-180');
                }});
            }});
        </script>
    ''')

