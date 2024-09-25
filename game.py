from PIL import ImageGrab, Image
import os
import pyautogui

### Розділення зображення на окремі клітинки

def split_image_into_cells(image, rows, cols, cell_width=74, cell_height=49):
    cells = []
    for row in range(rows):
        row_cells = []
        for col in range(cols):
            left = col * cell_width
            upper = row * cell_height
            right = left + cell_width
            lower = upper + cell_height
            cell = image.crop((left, upper, right, lower))
            # cell.save(f'temp/cell{row}-{col}.png')
            row_cells.append(cell)
        cells.append(row_cells)
    return cells

### Порівняння кожної клітинки з еталонними зображеннями

def load_templates(template_folder):
    templates = {}
    for filename in os.listdir(template_folder):
        if filename.endswith('.png'):
            key = os.path.splitext(filename)[0]
            template_image = Image.open(os.path.join(template_folder, filename))
            templates[key] = template_image
    return templates

def compare_images(img1, img2):
    histogram1 = img1.histogram()
    histogram2 = img2.histogram()
    score = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(histogram1, histogram2)) / len(histogram1)
    return score

def identify_cell(cell_image, templates):
    max_score = 0
    identified = None
    for key, template in templates.items():
        score = compare_images(cell_image, template)
        if score > max_score:
            max_score = score
            identified = key
    return identified

### Створення представлення поля у вигляді двовимірного масиву

def get_game_state(cells, templates):
    game_state = []
    for row_cells in cells:
        row_state = []
        for cell in row_cells:
            cell_id = identify_cell(cell, templates)
            row_state.append(cell_id)
        game_state.append(row_state)
    return game_state

### Розробка алгоритму для проходження рівня

def find_safe_cells(game_state):
    # Простий алгоритм для знаходження безпечних клітинок
    safe_cells = []
    rows = len(game_state)
    cols = len(game_state[0])
    for i in range(rows):
        for j in range(cols):
            if game_state[i][j] == '0':  # Якщо клітинка пуста
                neighbors = get_neighbors(game_state, i, j)
                for (ni, nj) in neighbors:
                    if game_state[ni][nj] == 'closed':
                        safe_cells.append((ni, nj))
    return safe_cells

def get_neighbors(game_state, row, col):
    rows = len(game_state)
    cols = len(game_state[0])
    neighbors = []
    for i in range(max(0, row -1), min(rows, row + 2)):
        for j in range(max(0, col -1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

### Автоматизація взаємодії з грою

def click_cell(x, y, cell_width, cell_height, top_left_x, top_left_y):
    cell_x = top_left_x + x * cell_width + cell_width // 2
    cell_y = top_left_y + y * cell_height + cell_height // 2
    pyautogui.click(cell_x, cell_y)

### Пошук ігрового поля

def search_game_field():
    # Вказуємо шлях до шаблону зображення ігрового поля
    game_field_image = 'templates/Maps/game_field_template.png'

    try:
        locations = list(pyautogui.locateAllOnScreen(game_field_image, confidence=0.7))
        if locations:
            print(f"Знайдено {len(locations)} збігів.")
            location = locations[0]
            # Розпаковуємо координати та розміри
            x, y, width, height = location
            screenshot = pyautogui.screenshot(region=(int(x+10), int(y+160), int(446), int(444)))
            screenshot.save('game_field_screenshot.png')
            # print("Скріншот ігрового поля збережено як 'game_field_screenshot.png'")
            return screenshot
        else:
            print("Ігрове поле не знайдено на екрані.")
    except pyautogui.ImageNotFoundException:
        print("Зображення не знайдено на екрані.")
    except Exception as e:
        print(f"Виникла помилка: {e}")


### Основна функція

def play_minesweeper():

    print("Start Bot...");

    rows = 9
    cols = 6

    # Захоплюємо знімок екрану
    screenshot = search_game_field()

    # Розбиваємо зображення на клітинки
    cells = split_image_into_cells(screenshot, rows, cols)

    # Завантажуємо еталонні зображення
    templates = load_templates('templates/Objects')

    # Отримуємо стан ігрового поля
    game_state = get_game_state(cells, templates)

    for row in game_state:
        print("\t".join(str(element) if element is not None else "None" for element in row))

    #
    # # Знаходимо безпечні клітинки для натискання
    # safe_cells = find_safe_cells(game_state)
    #
    # # Розраховуємо розмір клітинки
    # cell_width = w // cols
    # cell_height = h // rows

    # # Натискаємо на безпечні клітинки
    # #for (i, j) in safe_cells:
    # #   click_cell(j, i, cell_width, cell_height, x, y)
    # #    time.sleep(0.1)  # Невелика затримка між натисканнями
