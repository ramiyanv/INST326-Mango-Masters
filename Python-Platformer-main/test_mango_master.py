import os
import sys
import importlib
import pytest

# Prevent pygame trying to open a real window
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture
def mm(monkeypatch):
    """
    Import MangoMasters from the Python-Platformer-main folder, and patch out
    asset-heavy helpers so tests don't depend on image files.
    """
    # Ensure we import from the folder containing MangoMasters.py
    THIS_DIR = os.path.dirname(__file__)  # Python-Platformer-main
    if THIS_DIR not in sys.path:
        sys.path.insert(0, THIS_DIR)

    # Import (or reload) module
    mod = importlib.import_module("MangoMasters")
    mod = importlib.reload(mod)

    # Make sure pygame is initialized in a headless-friendly way
    mod.pygame.display.init()
    mod.pygame.display.set_mode((1, 1))

    # --- Patch helper functions used by Block / Player / Mango ---
    def solid_surface(w, h):
        surf = mod.pygame.Surface((w, h), mod.pygame.SRCALPHA)
        surf.fill((255, 255, 255, 255))  # opaque so mask collisions work
        return surf

    # Patch get_block so Block() doesn't load Terrain.png
    monkeypatch.setattr(mod, "get_block", lambda size: solid_surface(size * 2, size * 2))

    # Patch load_sprite_sheets so Player sprites don't load PNGs
    def fake_load_sprite_sheets(dir1, dir2, width, height, direction=False):
        surf = solid_surface(width * 2, height * 2)
        if direction:
            # Player.update_sprite expects keys like "idle_left", "idle_right", etc.
            return {
                "idle_left": [surf],
                "idle_right": [surf],
                "run_left": [surf],
                "run_right": [surf],
                "jump_left": [surf],
                "jump_right": [surf],
                "double_jump_left": [surf],
                "double_jump_right": [surf],
                "fall_left": [surf],
                "fall_right": [surf],
                "hit_left": [surf],
                "hit_right": [surf],
            }
        return {"off": [surf], "on": [surf]}

    monkeypatch.setattr(mod, "load_sprite_sheets", fake_load_sprite_sheets)

    # ALSO override Player.SPRITES directly (it was set at import time)
    mod.Player.SPRITES = fake_load_sprite_sheets("x", "y", 32, 32, True)

    # Patch pygame.image.load for Mango() so it doesn't need a real mango.png
    monkeypatch.setattr(mod.pygame.image, "load", lambda *args, **kwargs: solid_surface(20, 20))

    return mod


# -------------------- Tests (10+ total) --------------------

def test_flip_returns_list_of_surfaces(mm):
    s = mm.pygame.Surface((10, 10), mm.pygame.SRCALPHA)
    out = mm.flip([s])
    assert isinstance(out, list)
    assert len(out) == 1


def test_player_creation_defaults(mm):
    p = mm.Player(10, 20, 30, 40)
    assert p.rect.x == 10
    assert p.rect.y == 20
    assert p.score == 0
    assert p.direction in ("left", "right")


def test_player_move_left_and_right_changes_velocity_and_direction(mm):
    p = mm.Player(0, 0, 10, 10)
    p.move_left(5)
    assert p.x_vel == -5
    assert p.direction == "left"

    p.move_right(7)
    assert p.x_vel == 7
    assert p.direction == "right"


def test_player_jump_increments_jump_count_and_sets_negative_y_velocity(mm):
    p = mm.Player(0, 0, 10, 10)
    p.jump()
    assert p.jump_count == 1
    assert p.y_vel < 0


def test_player_landed_resets_vertical_motion(mm):
    p = mm.Player(0, 0, 10, 10)
    p.y_vel = 99
    p.fall_count = 10
    p.jump_count = 2

    p.landed()
    assert p.y_vel == 0
    assert p.fall_count == 0
    assert p.jump_count == 0


def test_block_creation_has_mask_and_position(mm):
    b = mm.Block(100, 200, 32)
    assert b.rect.topleft == (100, 200)
    assert hasattr(b, "mask")


def test_block_destroy_clears_mask_collision(mm):
    b = mm.Block(0, 0, 32)
    # After destroy(), it should be transparent => mask mostly empty
    b.destroy()
    # mask count should be 0 or very close to 0
    assert b.mask.count() == 0


def test_fire_toggle_switches_on_off(mm):
    f = mm.Fire(0, 0, 16, 32)
    assert f.animation_name in ("off", "on")

    f.on()
    assert f.animation_name == "on"

    f.toggle()
    assert f.animation_name == "off"

    f.toggle()
    assert f.animation_name == "on"


def test_mango_creation_has_name_and_mask(mm):
    m = mm.Mango(0, 0, 20, 20)
    assert m.name == "mango"
    assert hasattr(m, "mask")
    assert m.rect.width == 20
    assert m.rect.height == 20


def test_collide_returns_none_when_no_objects(mm):
    p = mm.Player(0, 0, 10, 10)
    p.update_sprite()
    hit = mm.collide(p, [], dx=5)
    assert hit is None


def test_handle_vertical_collision_lands_player_on_block(mm):
    """
    Interaction test: force a real mask overlap, then verify landing behavior.
    """
    p = mm.Player(0, 0, 32, 32)
    p.update_sprite()

    block = mm.Block(0, 50, 32)

    # Force overlap: put player inside block while "falling"
    p.rect.x = block.rect.x
    p.rect.y = block.rect.y - 10  # overlap a bit
    p.update()  # rebuild mask based on sprite

    p.y_vel = 5
    collided = mm.handle_vertical_collision(p, [block], dy=p.y_vel)

    assert block in collided
    assert p.y_vel == 0  # landed() should reset y_vel


def test_get_background_raises_filenotfound_for_missing_file(mm, monkeypatch):
    # Force background path check to fail
    monkeypatch.setattr(mm.os.path, "exists", lambda path: False)
    with pytest.raises(FileNotFoundError):
        mm.get_background("DefinitelyMissing.png")

