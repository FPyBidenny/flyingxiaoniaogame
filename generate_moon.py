from PIL import Image, ImageDraw

CELL_W = 280
CELL_H = 280
mr = 60  # 月亮半径，游戏中实际绘制尺寸为 120px（大大月亮）

sheet = Image.new('RGBA', (CELL_W * 4, CELL_H), (0, 0, 0, 0))

def draw_moon_phase(cell_x, phase):
    cx = cell_x * CELL_W + CELL_W // 2
    cy = CELL_H // 2

    # 1. 光晕：圆形径向渐隐，确保不碰到方形边界，避免光晕看起来是方的
    glow_layer = Image.new('RGBA', (CELL_W, CELL_H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_r = 110  # 光晕外半径，小于单元格一半，给透明边留余量
    for r in range(glow_r, 0, -1):
        t = r / glow_r
        # 中心亮，边缘透明；提高 alpha 让月亮在夜晚更明显
        alpha = int((1 - t) * 0.45 * 255)
        glow_draw.ellipse(
            [CELL_W // 2 - r, CELL_H // 2 - r,
             CELL_W // 2 + r, CELL_H // 2 + r],
            fill=(255, 255, 220, alpha)
        )
    # 将光晕贴到精灵图
    sheet.paste(glow_layer, (cell_x * CELL_W, 0), glow_layer)

    draw = ImageDraw.Draw(sheet)

    # 2. 月亮主盘（纯色圆，不带环形山，避免"左边小圆"）
    moon_color = (255, 253, 230, 255)
    draw.ellipse([cx - mr, cy - mr, cx + mr, cy + mr], fill=moon_color)

    # 3. 阴影：在独立图层绘制，再用月亮圆形 mask 裁剪
    if phase != 0:
        shadow_layer = Image.new('RGBA', (CELL_W, CELL_H), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        # 阴影改浅、半透明，不再像黑洞一样突兀，让月亮暗部仍能看清
        shadow_color = (60, 65, 95, 150)

        if phase == 1:
            shadow_draw.ellipse(
                [CELL_W // 2 + mr * 0.5 - mr * 0.85,
                 CELL_H // 2 - mr * 0.85,
                 CELL_W // 2 + mr * 0.5 + mr * 0.85,
                 CELL_H // 2 + mr * 0.85],
                fill=shadow_color
            )
        elif phase == 2:
            shadow_draw.pieslice(
                [CELL_W // 2 - mr, CELL_H // 2 - mr,
                 CELL_W // 2 + mr, CELL_H // 2 + mr],
                -90, 90, fill=shadow_color
            )
        elif phase == 3:
            shadow_draw.ellipse(
                [CELL_W // 2 + mr * 0.7 - mr * 0.78,
                 CELL_H // 2 - mr * 0.78,
                 CELL_W // 2 + mr * 0.7 + mr * 0.78,
                 CELL_H // 2 + mr * 0.78],
                fill=shadow_color
            )

        mask = Image.new('L', (CELL_W, CELL_H), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            [CELL_W // 2 - mr, CELL_H // 2 - mr,
             CELL_W // 2 + mr, CELL_H // 2 + mr],
            fill=255
        )
        sheet.paste(shadow_layer, (cell_x * CELL_W, 0), mask)

for phase in range(4):
    draw_moon_phase(phase, phase)

sheet.save('flappy-deploy/moon.png')
sheet.save('moon.png')
print('moon.png regenerated (280x280 per cell, mr=60, round glow, no craters)')
