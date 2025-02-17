document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    function addReactionListeners(context) {
        const reactionLinks = context.querySelectorAll('.reaction');
        reactionLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const reactionType = this.getAttribute('data-reaction');
                const commentId = this.getAttribute('data-comment-id');

                if (!reactionType || !commentId) return;

                socket.emit('new_reaction', {
                    forum_id: window.location.pathname.split('/').pop(),
                    comment_id: commentId,
                    reaction: reactionType
                });
            });
        });
    }

    // Mettre à jour le compteur en cas d'ajout de réaction
    socket.on('reaction_added', function(data) {
        const reactionCountElement = document.getElementById(`${data.reaction_type}-count-${data.comment_id}`);
        if (reactionCountElement) {
            reactionCountElement.textContent = data.reaction_count;
        }
    });

    // Mettre à jour le compteur en cas de suppression de réaction
    socket.on('reaction_removed', function(data) {
        const reactionCountElement = document.getElementById(`${data.reaction_type}-count-${data.comment_id}`);
        if (reactionCountElement) {
            reactionCountElement.textContent = data.reaction_count;
        }
    });

    addReactionListeners(document);
});
