function get_syn_path() {
    let $PathShow = $('#PathShow')
    $.post('/api/syn/path', {}, function (data) {
            $(data['results']).each(function () {
                    let a = $PathShow.append("<div class=\"card\">\n" +
                        "  <div class=\"card-header\">\n" +
                        "  </div>\n" +
                        "  <div class=\"card-body\">\n" +
                        "    <blockquote class=\"blockquote mb-0\">\n" +
                        "      <p>" + "ID:" + this['id'] + "</p>\n" +
                        "      <p><small>" + "源地址:" + this['source_path'] + "</small></p>\n" +
                        "      <p><small>" + "目标剧集地址:" + this['target_tv_path'] + "</small></p>\n" +
                        "      <p><small>" + "目标电影地址:" + this['target_movie_path'] + "</small></p>\n" +
                        "    </blockquote>\n" +
                        "  </div>\n" +
                        "</div>")
                    a.data('id', this['id'])
                    console.log(a.data('id'))
                }
            );
            $PathShow.addClass('mt-auto')
        }
    )
}

function add_path() {
    $('#sub').click(function () {
            $.post('/api/syn/add_path', {
                    'source_path': $('input#source_path').val(),
                    'target_tv_path': $('input#target_tv_path').val(),
                    'target_movie_path': $('input#target_movie_path').val()
                }, function () {
                    alert('提交成功')
                    $.reload()
                }
            )
        }
    )
}

function bind() {
    get_syn_path()
    add_path()
}

$(document).ready(bind)