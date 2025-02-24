from odoo import models, fields, api

class Round(models.Model):
    _name = "chessknight.round"
    _description = "Round Model"

    # Reference to the Tournament
    tournament_id = fields.Many2one(
        'chessknight.tournament',
        string='Tournament',
        required=True,
        ondelete='cascade',
        help='Tournament this round belongs to'
    )

    # Round Number
    round_number = fields.Integer(
        string='Round Number',
        required=True,
        help='Round number in the tournament'
    )

    # Status of the Round
    status = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed')
        ],
        string='Status',
        compute="_compute_status",
        default='scheduled',
        help='Current status of the round'
    )

    # Date fields for scheduling
    start_date = fields.Datetime(
        string='Start Date',
        help='Start date and time of the round'
    )

    end_date = fields.Datetime(
        string='End Date',
        help='End date and time of the round'
    )

    # Matches in this Round
    games = fields.One2many(
        'chessknight.game',
        'round_id',
        string='Games',
        help='Games in this round'
    )

   # Computed Name Field - Not Stored in Database
    name = fields.Char(
        string='Round Name',
        compute='_compute_name',
        store=False,  # Do not store in database
        help='Name of the round (e.g., Round 1)'
    )

    # Winner of the Round
    winner = fields.Many2one(
        'chessknight.user',
        string='Winner',
        compute='_compute_winner',
        store=True,
        help='Player with the most wins in this round'
    )

    @api.depends('games.winner', 'status')
    def _compute_winner(self):
        for record in self:
            if record.status == 'completed':
                # Count wins for each player
                win_count = {}
                for game in record.games:
                    if game.winner:
                        winner_id = game.player1.id if game.winner == 'player1' else game.player2.id
                        if winner_id in win_count:
                            win_count[winner_id] += 1
                        else:
                            win_count[winner_id] = 1
                
                # Determine the player with the most wins
                if win_count:
                    max_wins = max(win_count.values())
                    winners = [player_id for player_id, count in win_count.items() if count == max_wins]
                    
                    record.winner = winners[0]
                else:
                    record.winner = False
            else:
                record.winner = False



    @api.depends('round_number')
    def _compute_name(self):
        for record in self:
            record.name = f"Round {record.round_number}" if record.round_number else "Unnamed Round"

    @api.depends('games.status')
    def _compute_status(self):
        for record in self:
            if all(game.status == 'completed' for game in record.games):
                record.status = 'completed'
            elif any(game.status == 'ongoing' for game in record.games):
                record.status = 'ongoing'
            else:
                record.status = 'scheduled'

