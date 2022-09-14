function start_search() {
    let $search_keyword = $('#search_keyword').val()
    let $ShowVideo = $('#ShowVideo').empty()
    $.post('/api/themoviedb/search', {'search_keyword': $search_keyword}, function (data) {
            let $results = $(data['results'][0])
            $results.each(function () {
                    $ShowVideo.append(
                        "<div class=\"media mt-4\">\n" +
                        "  <img src=\""+'https://image.tmdb.org/t/p/w1280'+this['image']+"\" class=\"mr-3\" alt=\"...\" style=\"object-fit: cover;height: 200px\">\n" +
                        "  <div class=\"media-body\">\n" +
                        "    <h5 class=\"mt-0\">"+ this['name'] +"</h5>\n" +
                        "    <p>原名 "+ this['origin_name'] +"</p>\n" +
                        "    <p>开播时间: "+ this['first_air_date'] +"</p>\n" +
                        "    <p>类型: "+ this['media_type'] +"</p>\n" +
                        "  </div>\n" +
                        "  <button class='btn btn-light'>添加</button>" +
                        "</div>"
                    )
                    let $button = $('#ShowVideo div:last-child button')
                    console.log($button)
                    $button.data('tmdb_id',this['id'])
                    $button.data('media_type',this['media_type'])
                    $button.click(add_follow)
                }
            )

        }
    )
}

function add_follow() {
    let tmdb_id = $(this).data('tmdb_id')
    let media_type = $(this).data('media_type')
    $.post('/api/themoviedb/add_follow',{
            'tmdb_id':tmdb_id,
            'media_type':media_type
        },
        function () {
            alert('添加成功')
        }
    )
    console.log()
}

function bind() {
    $('#sub_search').click(start_search)
}

$(document).ready(bind)