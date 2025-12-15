import os
import sys
import importlib
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


@pytest.fixture
def mm(monkeypatch):
    """
    Import MangoMasters from the Python-Platformer-main folder, and patch out
    asset he avy helpers so tests dont depend on image files.
    """ 
   
    THIS_DIR = os.path.dirname(__file__) 
    if THIS_DIR not in sys.path:
        sys.path.insert(0, THIS_DIR)

    
    mod = importlib.import_module("MangoMasters")
    mod = importlib.reload(mod)

    
    mod.pygame.display.init()
    mod.pygame.display.set_mode((1, 1))

    
    def solid_surface(w, h):
        surf = mod.pygame.Surface((w, h), mod.pygame.SRCALPHA)
        surf.fill((255, 255, 255, 255)) 
        return surf

 
    monkeypatch.setattr(mod, "get_block", lambda size: solid_surface(size * 2, size * 2))

   
    def fake_load_sprite_sheets(dir1, dir2, width, height, direction=False):
        surf = solid_surface(width * 2, height * 2)
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
        return {"off": [surf], "on": [surf]}

    monkeypatch.setattr(mod, "load_sprite_sheets", fake_load_sprite_sheets)

    
    mod.Player.SPRITES = fake_load_sprite_sheets("x", "y", 32, 32, True)

    
    monkeypatch.setattr(mod.pygame.image, "load", lambda *args, **kwargs: solid_surface(20, 20))

    return mod




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
   
    b.destroy()

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

    
    p.rect.x = block.rect.x
    p.rect.y = block.rect.y - 10 
    p.update() 

    p.y_vel = 5
    collided = mm.handle_vertical_collision(p, [block], dy=p.y_vel)

    assert block in collided
    assert p.y_vel == 0 


def test_get_background_raises_filenotfound_for_missing_file(mm, monkeypatch):
    
    monkeypatch.setattr(mm.os.path, "exists", lambda path: False)
    with pytest.raises(FileNotFoundError):
        mm.get_background("DefinitelyMissing.png")

