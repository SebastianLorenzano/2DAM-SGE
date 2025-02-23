from xml.dom import ValidationErr
from odoo import models, fields, api

class Game(models.Model):
    _name = "chessknight.game"
    _description = "This is the game model"

    # One-to-One relationship simulated with Many2one and unique constraint
    player1 = fields.Many2one(
        'chessknight.user',  
        string='White Pieces',
        required=True,
        help='First player in the game',
        unique=True
    )
    
    player2 = fields.Many2one(
        'chessknight.user',
        string='Black Pieces',
        required=True,
        help='Second player in the game',
        unique=True
    )

        # Winner Field - Selection between player1 and player2
    winner = fields.Selection(
        selection=[
            ('player1', 'Player 1'),
            ('player2', 'Player 2')
        ],
        string='Winner',
        help='Select the winner of the game',
    )

        # Turn Counter - Must be positive
    turn = fields.Integer(
        string='Turn',
        default=1,
        help='Current turn number (must be positive)'
    )


    # Display the database ID as a read-only field
    game_id = fields.Char(
        string='Game ID',
        compute='_compute_game_id',  
        store=False, 
    )

    # This field is used as the display name
    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=False,
        help='Description of the field'
    )

    # Computed Field - Whose turn it is
    current_turn = fields.Char(
        string='Current Turn',
        compute='_compute_current_turn',
        store=False,
        help="Displays whose turn it is (White's or Black's)"
    )

    # Display Winner's Name
    winner_name = fields.Char(
        string='Winner Name',
        compute='_compute_winner_name',
        store=False
    )

    # Constraint to ensure player1 and player2 are not the same
    _sql_constraints = [
        ('check_players_diff', 
         'CHECK (player1 != player2)', 
         'Player 1 and Player 2 must be different users.')
    ]

    # Method to compute game_id field without @api.depends
    def _compute_game_id(self):
        for record in self:
            record.game_id = f"Game #{record.id}"

    # Compute method for the name field
    @api.depends('player1', 'player2')
    def _compute_name(self):
        for record in self:
            # Check if players are assigned
            player1_name = record.player1.name if record.player1 else "Unknown"
            player2_name = record.player2.name if record.player2 else "Unknown"

            # Assign a value to the name field
            record.name = f"Game #{record.id}: {player1_name} vs {player2_name}"

    # Compute the Winner's Name
    @api.depends('winner', 'player1', 'player2')
    def _compute_winner_name(self):
        for record in self:
            if record.winner == 'player1':
                record.winner_name = record.player1.name
            elif record.winner == 'player2':
                record.winner_name = record.player2.name
            else:
                record.winner_name = "No Winner Yet"

    # Compute Current Turn
    @api.depends('turn')
    def _compute_current_turn(self):
        for record in self:
            if record.turn % 2 == 0:
                record.current_turn = "Black's turn"
            else:
                record.current_turn = "White's turn"

    # Client-side validation for Turn
    @api.onchange('turn')
    def _onchange_turn(self):
        if self.turn < 1:
            self.turn = 1  # Reset to 1 if invalid
            return {
                'warning': {
                    'title': "Invalid Turn Value",
                    'message': "Turn must be a positive integer.",
                }
            }

    # Backend validation as a safety net (optional)
    @api.constrains('turn')
    def _check_turn_positive(self):
        for record in self:
            if record.turn < 1:
                raise ValidationErr("Turn must be a positive integer.")