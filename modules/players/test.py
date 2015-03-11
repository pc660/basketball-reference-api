import all_players

a = all_players.all_players("http://www.basketball-reference.com","/players")
a.create_database()
a.access_player_url()
