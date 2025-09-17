$(document).ready(function() {
    $('#generateIdeas').click(function() {
        var inspirationId = $('#inspiration_id').val();
        if (!inspirationId) {
            alert('请先选择一个灵感');
            return;
        }
        
        $(this).prop('disabled', true);
        $(this).text('生成中...');
        
        $.ajax({
            url: '/creation/generate_ideas',
            type: 'POST',
            data: {
                inspiration_id: inspirationId
            },
            success: function(response) {
                $('#summary').val(response.ideas.join('\n\n'));
            },
            error: function() {
                alert('生成创意失败，请重试');
            },
            complete: function() {
                $('#generateIdeas').prop('disabled', false);
                $('#generateIdeas').text('基于灵感生成创意');
            }
        });
    });
});