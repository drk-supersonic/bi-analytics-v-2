"""
Утилиты для работы с приложением
"""
import streamlit as st
import streamlit.components.v1 as components
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
    
    # Стили для Material Icons (шрифт загружается через font_style.css)
    st.markdown("""
        <style>
        span.material-icons {
            font-family: 'Material Icons' !important;
            font-weight: normal !important;
            font-style: normal !important;
            font-size: 24px !important;
            line-height: 1 !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            display: inline-block !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            -webkit-font-smoothing: antialiased !important;
            text-rendering: optimizeLegibility !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # JavaScript через components.html для правильного выполнения
    components.html("""
        <script>
        (function() {
            function applyMaterialIcons() {
                try {
                    var allSpans = document.querySelectorAll('span');
                    var materialIconNames = [
                        'keyboard_arrow_right', 'keyboard_arrow_left', 'keyboard_arrow_up', 'keyboard_arrow_down',
                        'arrow_right', 'arrow_left', 'arrow_up', 'arrow_down', 'arrow_forward', 'arrow_back'
                    ];
                    
                    for (var i = 0; i < allSpans.length; i++) {
                        var span = allSpans[i];
                        var text = (span.textContent || span.innerText || '').trim();
                        
                        var isIcon = false;
                        for (var j = 0; j < materialIconNames.length; j++) {
                            if (text === materialIconNames[j]) {
                                isIcon = true;
                                break;
                            }
                        }
                        
                        if (isIcon || 
                            (text.indexOf('keyboard_arrow') !== -1 && text.length < 25) ||
                            (text.indexOf('arrow_') === 0 && text.length < 20)) {
                            span.classList.add('material-icons');
                            span.style.fontFamily = "'Material Icons'";
                            span.style.fontSize = '24px';
                            span.style.lineHeight = '1';
                        }
                    }
                } catch(e) {
                    console.error('Error applying Material Icons:', e);
                }
            }
            
            function runApplyIcons() {
                applyMaterialIcons();
                setTimeout(applyMaterialIcons, 50);
                setTimeout(applyMaterialIcons, 100);
                setTimeout(applyMaterialIcons, 200);
                setTimeout(applyMaterialIcons, 500);
                setTimeout(applyMaterialIcons, 1000);
            }
            
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', runApplyIcons);
            } else {
                runApplyIcons();
            }
            
            if (typeof MutationObserver !== 'undefined') {
                var observer = new MutationObserver(applyMaterialIcons);
                if (document.body) {
                    observer.observe(document.body, {
                        childList: true,
                        subtree: true,
                        characterData: true
                    });
                }
            }
        })();
        </script>
    """, height=0)


def load_css_custom(css_content: str):
    """
    Применяет кастомные CSS стили
    
    Args:
        css_content: Строка с CSS стилями
    """
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

