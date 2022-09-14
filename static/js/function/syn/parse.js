function get_parse_file() {
    var $FileShow = $('#FileShow')
    $.post('/api/syn/parse_file', {}, function (data) {
            $(data['results']).each(function () {
                    $FileShow.append("<div class=\"card\">\n" +
                        "  <div class=\"card-header\">\n" +
                        "第" + this['season'] + '季 ' + "第" + this['episode'] + '集' + //季与集
                        "    \n" +
                        "  </div>\n" +
                        "  <div class=\"card-body\">\n" +
                        "    <blockquote class=\"blockquote mb-0\">\n" +
                        "      <p>" + this['name'] + "</p>\n" +
                        "      <small>" + this['file_path'] + "</small>\n" +
                        "    </blockquote>\n" +
                        "  </div>\n" +
                        "</div>")
                    //$a.addClass('mt-auto')
                    //$('.card :last-child').data('id', this['id']).addClass('mt-auto')
                }
            );
        }
    )
}

$(document).ready(get_parse_file)