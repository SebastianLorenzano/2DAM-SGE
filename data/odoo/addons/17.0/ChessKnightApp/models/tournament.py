from odoo import models, fields, api

class Tournament(models.Model):
    _name = "chessknight.tournament"
    _description = "Tournament Model"

    name = fields.Char(
        string='Tournament Name',
        required=True,
        help='Name of the tournament'
    )

    date = fields.Date(
        string='Date',
        required=True,
        help='Date of the tournament'
    )

    status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='scheduled',
        help='Current status of the tournament'
    )

    format = fields.Selection(
        selection=[
            ('swiss', 'Swiss'),
            ('round_robin', 'Round Robin'),
            ('knockout', 'Knockout')
        ],
        string='Format',
        required=True,
        default='swiss',
        help='Tournament format type'
    )

    number_of_rounds = fields.Integer(
        string='Number of Rounds',
        default=1,
        help='Number of rounds in the tournament'
    )

    # Rounds in this Tournament
    rounds = fields.One2many(
        'chessknight.round',
        'tournament_id',
        string='Rounds',
        help='Rounds in this tournament'
    )

    # Use Many2many to link multiple players to a tournament
    players = fields.Many2many(
        'chessknight.user',                # Related model
        'chessknight_tournament_user_rel', # Relation table
        'tournament_id',                   # Column in the relation table for this model
        'user_id',                         # Column in the relation table for the related model
        string='Players',
        help='Players participating in this tournament'
    )

    # Winner Field - Must be one of the selected players
    winner = fields.Many2one(
        'chessknight.user',
        string='Winner',
        help='Select the winner of the tournament',
        domain="[('id', 'in', players)]"   # Use players to restrict winner choices
    )

    @api.onchange('players')
    def _onchange_players(self):
        # Clear the winner if it's not in the players list
        if self.winner and self.winner not in self.players:
            self.winner = False

    @api.depends('players')
    def _compute_winner_domain(self):
        for record in self:
            # Get all the player IDs in the tournament
            player_ids = record.players.ids if record.players else []
            # Store the domain in a computed field (not shown)
            record.winner_domain = [('id', 'in', player_ids)]