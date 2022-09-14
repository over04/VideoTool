function start_search() {
    let $search_keyword = $('#search_keyword').val()
    let $ShowVideo = $('#ShowVideo').empty()
    $.post('/api/themoviedb/search_best', {'search_keyword': $search_keyword}, function (data) {
            let img_url = 'https://image.tmdb.org/t/p/w1280' + data['results']['image']
            $.post('/api/jackett/search', {'search_keyword': $search_keyword}, function (data) {
                    let $results = $(data['results'])
                    $results.each(function () {
                            $ShowVideo.append(
                                "<div class=\"media mt-4\">\n" +
                                "  <img src=\"" + img_url + "\" class=\"mr-3\" alt=\"...\" style=\"object-fit: cover;height: 200px\">\n" +
                                "  <div class=\"media-body\">\n" +
                                "    <h5 class=\"mt-0\">" + this['name'] + "</h5>\n" +
                                "    <p>原名 " + this['origin_name'] + "</p>\n" +
                                "    <p>集数: " + this['episode'][0] + "</p>\n" +
                                "    <p>季数: " + this['season'] + "</p>\n" +
                                "  </div>\n" +
                                "  <button class='btn btn-light'>下载</button>" +
                                "</div>"
                            )
                            let $button = $('#ShowVideo div:last-child button')
                            console.log($button)
                            $button.data('download_url', this['url'])
                            $button.click(download_url)
                        }
                    )
                }
            )

        }
    )
}

function download_url() {
    let download_url = $(this).data('download_url')
    $.post('/api/qbittorrent/download', {
            'url': download_url
        },
        function () {
            alert('添加下载成功')
        }
    )
    console.log()
}

function bind() {
    $('#sub_search').click(start_search)
}

$(document).ready(bind)