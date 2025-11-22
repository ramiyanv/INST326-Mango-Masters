import pytest
from HW_1_Ramiyan_Varghese import GameCharacter  

def test_initial_state():
    test1 = GameCharacter("Test001")
    assert test1.character_id == "Test001"
    assert test1.get_position() == (0, 0)
    assert test1.get_resource_level("health") == 100.0
    assert test1.get_resource_level("energy") == 50.0
    assert test1.get_resource_level("stamina") == 30.0
    assert test1.inventory == {}

def test_movement():
    test1 = GameCharacter("Test001")
    test1.move_up()
    assert test1.get_position() == (0, 1)
    test1.move_right()
    assert test1.get_position() == (1, 1)
    test1.move_down()
    assert test1.get_position() == (1, 0)
    test1.move_left()
    assert test1.get_position() == (0, 0)

def test_collect_and_drop_items():
    test1 = GameCharacter("Test001")
    test1.collect_item("potion", 2)
    assert test1.inventory["potion"] == 2
    test1.collect_item("potion", 1)
    assert test1.inventory["potion"] == 3
    test1.drop_item("potion")
    assert test1.inventory["potion"] == 2
    test1.drop_item("potion")
    test1.drop_item("potion")  
    assert "potion" not in test1.inventory

def test_use_resource():
    test1 = GameCharacter("Test001")
    test1.use_resource("health", 20)
    assert test1.get_resource_level("health") == 80.0
    test1.use_resource("energy", 60) 
    assert test1.get_resource_level("energy") == 0.0

def test_replenish_resource():
    test1 = GameCharacter("Test001")
    test1.use_resource("health", 90)
    test1.replenish_resource("health", 15)
    assert test1.get_resource_level("health") == 25.0

def test_reset_position():
    test1 = GameCharacter("Test001")
    test1.move_up()
    test1.move_right()
    assert test1.get_position() == (1, 1)
    test1.reset_position()
    assert test1.get_position() == (0, 0)

def test_multiple_characters():
    hero1 = GameCharacter("Hero001")
    support1 = GameCharacter("Support002")

    hero1.move_right()
    support1.move_left()
    assert hero1.get_position() == (1, 0)
    assert support1.get_position() == (-1, 0)

    hero1.collect_item("sword", 1)
    support1.collect_item("shield", 1)
    assert hero1.inventory["sword"] == 1
    assert support1.inventory["shield"] == 1

    hero1.use_resource("stamina", 15)
    support1.use_resource("stamina", 10)
    assert hero1.get_resource_level("stamina") == 15.0
    assert support1.get_resource_level("stamina") == 20.0


    assert hero1.character_id == "Hero001"
    assert support1.character_id == "Support002"