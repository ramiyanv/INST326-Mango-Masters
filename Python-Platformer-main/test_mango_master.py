import os

# Prevent pygame from opening a real window during import
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import importlib
import pytest


@pytest.fixture
def mm(monkeypatch):
    """
    Import MangoMasters safely and mock asset-loading helpers so tests
    don't depend on external image files.
    """
    mod = importlib.import_module("MangoMasters")

    # ---- mock load_sprite_sheets so Player/Fire animations don't need real files ----
    def fake_load_sprite_sheets(dir1, dir2, width, height, direction=False):
        surf = mod.pygame.Surface((width, height), mod.pygame.SRCALPHA)
        if direction:
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
        # Fire uses keys "off" and "on"
        return {"off": [surf], "on": [surf]}

    monkeypatch.setattr(mod, "load_sprite_sheets", fake_load_sprite_sheets, raising=True)

    # Player.SPRITES is set at import-time; override it for tests.
    mod.Player.SPRITES = fake_load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)

    # ---- mock get_block so Block doesn't load Terrain.png ----
    def fake_get_block(size):
        return mod.pygame.Surface((size, size), mod.pygame.SRCALPHA)

    monkeypatch.setattr(mod, "get_block", fake_get_block, raising=True)

    # ---- avoid Mango file IO by replacing Mango.__init__ ----
    def fake_mango_init(self, x, y, width, height):
        mod.Object.__init__(self, x, y, width, height, "mango")
        self.image = mod.pygame.Surface((width, height), mod.pygame.SRCALPHA)
        self.mask = mod.pygame.mask.from_surface(self.image)

    monkeypatch.setattr(mod.Mango, "__init__", fake_mango_init, raising=True)

    return mod


# -------------------- Happy-path tests --------------------

def test_flip_returns_list_of_surfaces(mm):
    s = mm.pygame.Surface((10, 10), mm.pygame.SRCALPHA)
    out = mm.flip([s, s])
    assert isinstance(out, list)
    assert len(out) == 2
    assert all(isinstance(x, mm.pygame.Surface) for x in out)


def test_player_creation_defaults(mm):
    p = mm.Player(100, 200, 50, 50)
    assert p.rect.topleft == (100, 200)
    assert p.x_vel == 0
    assert p.y_vel == 0
    assert p.direction == "left"
    assert p.score == 0
    assert p.jump_count == 0


def test_player_move_left_and_right_changes_velocity_and_direction(mm):
    p = mm.Player(0, 0, 10, 10)
    p.move_right(5)
    assert p.x_vel == 5
    assert p.direction == "right"

    p.move_left(7)
    assert p.x_vel == -7
    assert p.direction == "left"


def test_player_jump_increments_jump_count_and_sets_negative_y_velocity(mm):
    p = mm.Player(0, 0, 10, 10)
    p.jump()
    assert p.jump_count == 1
    assert p.y_vel < 0  # jump goes up


def test_player_landed_resets_vertical_motion(mm):
    p = mm.Player(0, 0, 10, 10)
    p.jump()
    p.y_vel = 5
    p.fall_count = 99

    p.landed()
    assert p.y_vel == 0
    assert p.fall_count == 0
    assert p.jump_count == 0


def test_block_creation_has_mask_and_position(mm):
    b = mm.Block(10, 20, 32)
    assert b.rect.topleft == (10, 20)
    assert b.mask is not None


def test_fire_toggle_switches_on_off(mm):
    f = mm.Fire(0, 0, 16, 32)
    assert f.animation_name == "off"
    f.toggle()
    assert f.animation_name == "on"
    f.toggle()
    assert f.animation_name == "off"


def test_mango_creation_has_name_and_mask(mm):
    m = mm.Mango(5, 6, 12, 13)
    assert m.name == "mango"
    assert m.mask is not None


# -------------------- Interaction + edge-case tests --------------------

def test_block_destroy_makes_block_non_solid_for_mask_collision(mm):
    """
    Edge-ish case: after destroy, the block image becomes transparent.
    We confirm the mask has no filled pixels.
    """
    b = mm.Block(0, 0, 32)
    b.destroy()
    assert b.mask.count() == 0  # no opaque pixels => no collision area


def test_collide_returns_none_when_no_objects(mm):
    """
    Happy-path: no objects => no collision.
    """
    p = mm.Player(0, 0, 10, 10)
    p.update_sprite()
    hit = mm.collide(p, [], dx=5)
    assert hit is None


def test_handle_vertical_collision_lands_player_on_block(mm, monkeypatch):
    """
    Interaction test: verify handle_vertical_collision logic when a collision occurs.
    We patch collide_mask to force a collision so this test doesn't depend on sprite pixels.
    """
    p = mm.Player(0, 0, 10, 10)
    block = mm.Block(0, 20, 32)

    # Force collision regardless of masks
    monkeypatch.setattr(mm.pygame.sprite, "collide_mask", lambda a, b: True)

    p.y_vel = 5  # falling
    collided = mm.handle_vertical_collision(p, [block], dy=p.y_vel)

    assert block in collided
    assert p.rect.bottom == block.rect.top  # snapped onto the block
    assert p.y_vel == 0
    assert p.jump_count == 0



def test_object_draw_does_not_crash(mm):
    """
    Edge case: drawing should not crash even if object is simple surface.
    """
    win = mm.pygame.Surface((200, 200), mm.pygame.SRCALPHA)
    obj = mm.Object(10, 10, 20, 20, name="testobj")
    # should not raise
    obj.draw(win, offset_x=0)


def test_get_background_raises_filenotfound_for_missing_file(mm, monkeypatch):
    """
    Error condition: get_background should raise FileNotFoundError if the image is missing.
    We force os.path.exists to return False.
    """
    monkeypatch.setattr(mm.os.path, "exists", lambda path: False)
    with pytest.raises(FileNotFoundError):
        mm.get_background("does_not_exist.png")
