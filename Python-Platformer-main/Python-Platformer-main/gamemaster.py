
# GAMEMASTER CLASS (Separate - for team approval)

class GameMaster:
    
    def __init__(self):
        self.difficulty_level = 1
        self.score_multiplier = 1.0
        self.wave_number = 0
        self.events_log = []
        self.checkpoint_positions = []
        self.game_state = {
            'enemy_speed_modifier': 0,
            'time_scale': 1.0,
            'active_power_ups': []
        }
        
    def increase_difficulty(self):
        self.difficulty_level += 1
        self.score_multiplier += 0.1
        self.game_state['enemy_speed_modifier'] += 0.5
        self.events_log.append(f"Difficulty increased to level {self.difficulty_level}")
        return self.difficulty_level
    
    def spawn_enemy_wave(self, game_width=800, game_height=600, count=None):
        if count is None:
            count = 2 + self.difficulty_level
        
        self.wave_number += 1
        spawn_positions = []
        
        for _ in range(count):
            x = random.randint(50, game_width - 50)
            y = random.randint(50, 300)
            spawn_positions.append({'x': x, 'y': y})
        
        self.events_log.append(f"Wave {self.wave_number}: Generated {count} enemy spawn positions")
        return spawn_positions
    
    def create_checkpoint(self, x, y):
        checkpoint = {
            'x': x,
            'y': y,
            'activated': False,
            'id': len(self.checkpoint_positions)
        }
        self.checkpoint_positions.append(checkpoint)
        return checkpoint
    
    def activate_checkpoint(self, checkpoint_id):
        if checkpoint_id < len(self.checkpoint_positions):
            checkpoint = self.checkpoint_positions[checkpoint_id]
            checkpoint['activated'] = True
            self.events_log.append(f"Checkpoint {checkpoint_id} activated")
            return checkpoint
        return None
    
    def get_respawn_position(self, checkpoint_id=None):
        if checkpoint_id is not None and checkpoint_id < len(self.checkpoint_positions):
            checkpoint = self.checkpoint_positions[checkpoint_id]
            if checkpoint['activated']:
                self.events_log.append(f"Respawn at checkpoint {checkpoint_id}")
                return checkpoint['x'], checkpoint['y']
        
        self.events_log.append("Respawn at start position")
        return 100, 500
    
    def calculate_score_bonus(self, base_score, action_type="collect"):
        bonus_multipliers = {
            'collect': 1.0,
            'enemy_defeat': 2.0,
            'speed_bonus': 1.5,
            'no_damage': 2.5
        }
        
        multiplier = bonus_multipliers.get(action_type, 1.0)
        final_score = int(base_score * multiplier * self.score_multiplier)
        return final_score
    
    def check_win_condition(self, score, collectibles_remaining):
        if score >= 500:
            self.events_log.append("Win condition met: Score reached 500")
            return True
        
        if collectibles_remaining == 0 and score > 0:
            self.events_log.append("Win condition met: All collectibles gathered")
            return True
        
        return False
    
    def spawn_power_up(self, game_width=800, game_height=600, x=None, y=None, power_type=None):
        if x is None:
            x = random.randint(50, game_width - 50)
        if y is None:
            y = random.randint(50, game_height - 100)
        
        power_types = ['speed', 'jump', 'invincibility', 'health']
        if power_type is None:
            power_type = random.choice(power_types)
        
        power_up = {
            'x': x,
            'y': y,
            'type': power_type,
            'duration': 300,
            'active': True,
            'width': 25,
            'height': 25
        }
        
        self.game_state['active_power_ups'].append(power_up)
        self.events_log.append(f"Spawned {power_type} power-up at ({x}, {y})")
        return power_up


