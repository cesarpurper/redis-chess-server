var onDragStart = function (source, piece, position, orientation) {
                if ((orientation === 'white' && piece.search(/^w/) === -1) ||
                    (orientation === 'black' && piece.search(/^b/) === -1)) {
                    return false;
                }
            };

            var onDrop = function (source, target) {
                // see if the move is legal
                var move = game.move({
                    from: source,
                    to: target,
                    promotion: 'q' // NOTE: always promote to a queen for example simplicity
                });

                // illegal move
                if (move === null) return 'snapback';



                //update via clientJS
                //updateStatus();
            };


            // update the board position after the piece snap 
            // for castling, en passant, pawn promotion
           

            var updateStatus = function () {
                var status = '';

                var moveColor;
                if (game.turn() === 'b') {
                    $("#playing-player2").css("display", "inline")
                    $("#playing-player1").css("display", "none")
                    moveColor = 'Black';
                } else {
                    $("#playing-player2").css("display", "none")
                    $("#playing-player1").css("display", "inline")
                    moveColor = 'White';
                }

                // checkmate?
                if (game.in_checkmate() === true) {
                    status = 'Game over, ' + moveColor + ' is in checkmate.';
                }

                // draw?
                else if (game.in_draw() === true) {
                    status = 'Game over, drawn position';
                }

                // game still on
                else {
                    status = moveColor + ' to move';

                    // check?
                    if (game.in_check() === true) {
                        status += ', ' + moveColor + ' is in check';
                    }
                }

                statusEl.html(status);
                fenEl.html(game.fen());
                pgnEl.html(game.pgn());
            };