$(function() {
  $('a[data-issue]').each(function() {
    var issue_id = $(this).attr('data-issue');
    var link = $(this);
    $.ajax('/issues/'+issue_id+'.json', {
      dataType: 'json',
      success: function(issue) {
        link.popover({
          title: issue.__str__ + ' / ' + issue.title,
          content: issue.html_summary,
          html: true,
          placement: 'bottom',
          trigger: 'hover',
        });
      },
    });
  });
});
