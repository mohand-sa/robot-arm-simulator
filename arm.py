import pygame
import math

WIDTH, HEIGHT = 800, 600
ORIGIN = (WIDTH // 2, HEIGHT - 100)
SCALE = 25
L1, L2 = 8, 10
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
FLASH_DURATION = 10


def inverse_kinematics(x, y):
    r = math.hypot(x, y)
    if r > L1 + L2 or r < abs(L1 - L2):
        return None

    cos_theta2 = (r * r - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    cos_theta2 = max(-1.0, min(1.0, cos_theta2))
    theta2 = math.acos(cos_theta2)

    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))
    return math.degrees(theta1), math.degrees(theta2)


def draw_arm(screen, theta1_deg, theta2_deg):
    t1 = math.radians(theta1_deg)
    t2 = math.radians(theta1_deg + theta2_deg)

    x1 = L1 * math.cos(t1)
    y1 = L1 * math.sin(t1)
    x2 = x1 + L2 * math.cos(t2)
    y2 = y1 + L2 * math.sin(t2)

    sx1 = ORIGIN[0] + x1 * SCALE
    sy1 = ORIGIN[1] - y1 * SCALE
    sx2 = ORIGIN[0] + x2 * SCALE
    sy2 = ORIGIN[1] - y2 * SCALE

    shadow_offset = 3
    pygame.draw.line(screen, GRAY, (ORIGIN[0] + shadow_offset, ORIGIN[1] + shadow_offset), (sx1 + shadow_offset, sy1 + shadow_offset), 6)
    pygame.draw.line(screen, GRAY, (sx1 + shadow_offset, sy1 + shadow_offset), (sx2 + shadow_offset, sy2 + shadow_offset), 6)

    pygame.draw.line(screen, RED, ORIGIN, (sx1, sy1), 10)
    pygame.draw.line(screen, BLUE, (sx1, sy1), (sx2, sy2), 10)

    pygame.draw.circle(screen, BLACK, ORIGIN, 10)
    pygame.draw.circle(screen, BLACK, (int(sx1), int(sy1)), 8)
    pygame.draw.circle(screen, BLACK, (int(sx2), int(sy2)), 6)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    current_angles = [90.0, 0.0]
    target_angles = [90.0, 0.0]
    flash_counter = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                x = (mx - ORIGIN[0]) / SCALE
                y = -(my - ORIGIN[1]) / SCALE
                angles = inverse_kinematics(x, y)
                if angles:
                    target_angles[0], target_angles[1] = angles
                    flash_counter = 0
                else:
                    flash_counter = FLASH_DURATION

        c1, c2 = current_angles
        t1, t2 = target_angles

        dist1 = abs(c1 - t1)
        dist2 = abs(c2 - t2)

        speed1 = min(max(0.2, dist1 / 10), 5.0, dist1)
        speed2 = min(max(0.2, dist2 / 10), 5.0, dist2)

        if dist1 > 0.05:
            c1 += speed1 if c1 < t1 else -speed1
        else:
            c1 = t1

        if dist2 > 0.05:
            c2 += speed2 if c2 < t2 else -speed2
        else:
            c2 = t2

        current_angles = [c1, c2]

        if flash_counter > 0:
            screen.fill((255, 200, 200))
            flash_counter -= 1
        else:
            screen.fill(WHITE)

        draw_arm(screen, *current_angles)

        text = f"θ₁: {c1:.1f}° | θ₂: {c2:.1f}°"
        screen.blit(font.render(text, True, BLACK), (10, 10))

        pygame.draw.circle(screen, (200, 200, 200), ORIGIN, int((L1 + L2) * SCALE), 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
