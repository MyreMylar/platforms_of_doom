# -------------------------------------------------------
# Challenge
# -------------
#
# Create a PowerUp class and implement it into the 'platforms_of_doom'
# game (and code file) so that it meets the following goals
#
# - Displays on the screen as a small 16 pixel by 16 pixel
#   rectangle.
# - When touched by the player it 'dies' and is removed.
# - A power up is created in the game every 20 seconds.
# - The power ups appear on top of, and in the centre of,
#   the platforms.
#
# Hints
# --------
# - You will need to use a list in the game code file
#   to store the power ups after you create them.
#
# - Make things easy for yourself by looking at (and stealing)
#   code that has already been written for this game. For
#   example the platforms already render as simple rectangles
#   and the players already appear in the centre of, and on
#   top of the platforms.
#
# - There are examples of timers in several places in the
#   code. Look for variables ending in 'acc' where I add
#   'dt' or 'time_delta' which is just the (very small) difference
#   in time between the current update loop and the previous one.
#
# - We are just trying to get the basics of a power up
#   setup next week. Next time we'll go further and make
#   them do something more exciting.
#
# Extra credit
# --------------
#
#  - Stop more than two power ups from appearing at any one
#    time so the screen doesn't fill with power ups
#
#  - Make sure power ups don't spawn where there is already a power
#    up.
# --------------------------------------------------------
