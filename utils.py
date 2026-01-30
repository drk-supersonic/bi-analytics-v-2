"""
Утилиты для работы с приложением
"""
import streamlit as st
import os


def load_css(css_file_path: str = "static/css/style.css"):
    """
    Загружает CSS файл и применяет стили к приложению
    
    Args:
        css_file_path: Путь к CSS файлу относительно корня проекта
    """
    try:
        # Получаем путь к корню проекта
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, css_file_path)
        
        # Проверяем существование файла
        if not os.path.exists(css_path):
            st.warning(f"CSS файл не найден: {css_path}")
            return
        
        # Читаем CSS файл
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Применяем стили
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ошибка при загрузке CSS: {e}")


def load_fonts(font_css_path: str = "static/css/font_style.css"):
    """
    Загружает CSS файл со шрифтами и исправляет пути к файлам шрифтов
    Использует base64 для встраивания шрифтов прямо в CSS
    
    Args:
        font_css_path: Путь к CSS файлу со шрифтами относительно корня проекта
    """
    try:
        import base64
        import re
        
        # Получаем путь к корню проекта
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, font_css_path)
        
        # Проверяем существование файла
        if not os.path.exists(font_path):
            # Не показываем предупреждение, если файл не найден (шрифты опциональны)
            return
        
        # Читаем CSS файл
        with open(font_path, 'r', encoding='utf-8') as f:
            font_content = f.read()
        
        # Находим все пути к шрифтам и заменяем их на base64
        def replace_font_path(match):
            font_file = match.group(1)
            font_full_path = os.path.join(current_dir, "static", "fonts", font_file)
            
            if os.path.exists(font_full_path):
                try:
                    with open(font_full_path, 'rb') as f:
                        font_data = f.read()
                        font_base64 = base64.b64encode(font_data).decode('utf-8')
                        # Определяем формат по расширению и правильный MIME type
                        if font_file.endswith('.woff2'):
                            mime_type = 'font/woff2'
                        elif font_file.endswith('.woff'):
                            mime_type = 'font/woff'
                        elif font_file.endswith('.ttf'):
                            mime_type = 'font/ttf'
                        elif font_file.endswith('.otf'):
                            mime_type = 'font/otf'
                        else:
                            mime_type = 'font/woff2'
                        
                        return f"url('data:{mime_type};base64,{font_base64}')"
                except Exception:
                    # Если не удалось загрузить, возвращаем оригинальный путь
                    return match.group(0)
            else:
                # Если файл не найден, возвращаем оригинальный путь
                return match.group(0)
        
        # Заменяем все пути к шрифтам на base64
        # Поддерживаем разные форматы: url('../fonts/...'), url("../fonts/..."), url(../fonts/...)
        patterns = [
            r"url\('\.\./fonts/([^']+)'\)",  # url('../fonts/...')
            r'url\("\.\./fonts/([^"]+)"\)',   # url("../fonts/...")
            r'url\(\.\./fonts/([^)]+)\)',     # url(../fonts/...)
        ]
        
        for pattern in patterns:
            font_content = re.sub(pattern, replace_font_path, font_content)
        
        # Применяем стили
        st.markdown(f"<style>{font_content}</style>", unsafe_allow_html=True)
    except Exception as e:
        # Не показываем ошибку пользователю (шрифты опциональны)
        # Ошибки можно увидеть в логах сервера
        pass


def load_all_styles():
    """
    Загружает все CSS файлы: сначала шрифты, затем основные стили
    """
    load_fonts()
    load_css()
    
    # Скрываем текстовые артефакты Material Icons (например, keyboard_arrow_right)
    st.markdown("""
        <script>
        // Скрываем span элементы с именами Material Icons
        function hideMaterialIcons() {
            // Ищем все span элементы, которые содержат имена Material Icons
            const iconSpans = document.querySelectorAll('span[class*="material-icons"], span.material-icons, span[class*="keyboard_arrow"], span[class*="arrow_right"]');
            iconSpans.forEach(span => {
                const text = span.textContent || span.innerText;
                // Если текст содержит имя Material Icon (например, keyboard_arrow_right)
                if (text && (text.includes('keyboard_arrow') || text.includes('arrow_right') || text.includes('_arrow'))) {
                    span.style.display = 'none';
                    span.style.visibility = 'hidden';
                    span.style.width = '0';
                    span.style.height = '0';
                    span.style.fontSize = '0';
                    span.style.lineHeight = '0';
                }
            });
            
            // Также ищем span элементы с текстом, который является именем Material Icon
            const allSpans = document.querySelectorAll('span');
            allSpans.forEach(span => {
                const text = span.textContent || span.innerText;
                if (text && (text.trim() === 'keyboard_arrow_right' || 
                             text.trim().includes('keyboard_arrow') ||
                             text.trim().includes('arrow_right'))) {
                    span.style.display = 'none';
                    span.style.visibility = 'hidden';
                    span.style.width = '0';
                    span.style.height = '0';
                    span.style.fontSize = '0';
                    span.style.lineHeight = '0';
                }
            });
        }
        
        // Выполняем сразу и после загрузки DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hideMaterialIcons);
        } else {
            hideMaterialIcons();
        }
        
        // Также выполняем после обновления Streamlit
        setTimeout(hideMaterialIcons, 100);
        setInterval(hideMaterialIcons, 500);
        </script>
    """, unsafe_allow_html=True)


def load_css_custom(css_content: str):
    """
    Применяет кастомные CSS стили
    
    Args:
        css_content: Строка с CSS стилями
    """
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

