from odoo import models, fields, api

class User(models.Model):
    _name = "chessknight.user"
    _description = "This is the user model"

    name = fields.Char(
        string='Name',
        help='Description of the field')
    
    email = fields.Char(
        string='Email',
        help='Contact email of the player'
    )

    avatar = fields.Image(
        string='Avatar',
        max_width=128,
        max_height=128,
        help='Profile picture of the player'
    )

    bio = fields.Text(
        string='Bio',
        help='Brief biography of the player'
    )

        # Computed field to count all the games in 'games'
    game_count = fields.Integer(
        string='Games Played',
        compute='_compute_game_count',
        store=True,
        help='Total number of games this player has played'
    )

    # Computed field to count the games won by the player
    games_won_count = fields.Integer(
        string='Games Won',
        compute='_compute_games_won_count',
        store=True,
        help='Total number of games this player has won'
    )

    win_rate = fields.Float(
        string='Win Rate (%)',
        compute='_compute_win_rate',
        store=True,
        help='Percentage of games won by the player'
    )

    # Computed Many2many: A Player can play many Games as either player1 or player2
    games = fields.Many2many(
        'chessknight.game',      # Related model
        compute='_compute_games',# Compute method
        string='Games',
        help='Games this player has played as either Player 1 or Player 2'
    )


    # Many2many: A Player can participate in many Tournaments
    tournaments = fields.Many2many(
        'chessknight.tournament',          # Related model
        'chessknight_tournament_user_rel', # Relation table
        'user_id',                        # Column in the relation table for this model
        'tournament_id',                   # Column in the relation table for the related model
        string='Tournaments',
        help='Tournaments this player is participating in'
    )


    # New: Tournaments Played
    tournaments_played = fields.Integer(
        string='Tournaments Played',
        compute='_compute_tournaments_played',
        store=True,
        help='Total number of tournaments this player has played'
    )

    # New: Tournaments Won
    tournaments_won = fields.Integer(
        string='Tournaments Won',
        compute='_compute_tournaments_won',
        store=True,
        help='Total number of tournaments this player has won'
    )

        # Calculate Win Rate
    @api.depends('games_won_count', 'game_count')
    def _compute_win_rate(self):
        for record in self:
            if record.game_count > 0:
                record.win_rate = (record.games_won_count / record.game_count) * 100
            else:
                record.win_rate = 0.0

    # Collect all games where this player is either player1 or player2
    @api.depends('games', 'games.player1', 'games.player2')
    def _compute_games(self):
        for record in self:
            Game = self.env['chessknight.game']
            # Find all games where this player is either player1 or player2
            games_as_player1 = Game.search([('player1', '=', record.id)])
            games_as_player2 = Game.search([('player2', '=', record.id)])
            # Combine both lists of games
            record.games = games_as_player1 | games_as_player2

        # Count all games the player has played
    @api.depends('games', 'games.player1', 'games.player2')
    def _compute_game_count(self):
        for record in self:
            games_as_player1 = self.env['chessknight.game'].search_count([
                ('player1', '=', record.id)
            ])
            games_as_player2 = self.env['chessknight.game'].search_count([
                ('player2', '=', record.id)
            ])
            record.game_count = games_as_player1 + games_as_player2

    # Count the games the player won
    @api.depends('games', 'games.winner', 'games.player1', 'games.player2')
    def _compute_games_won_count(self):
        for record in self:
            games_won = self.env['chessknight.game'].search([
                '|',
                '&', ('player1', '=', record.id), ('winner', '=', 'player1'),
                '&', ('player2', '=', record.id), ('winner', '=', 'player2')
            ])
            record.games_won_count = len(games_won)


    # Count Tournaments Played
    @api.depends('tournaments')
    def _compute_tournaments_played(self):
        for record in self:
            record.tournaments_played = len(record.tournaments)

    # Count Tournaments Won
    @api.depends('tournaments')
    def _compute_tournaments_won(self):
        for record in self:
            tournaments_won = self.env['chessknight.tournament'].search_count([
                ('winner', '=', record.id)
            ])
            record.tournaments_won = tournaments_won


    