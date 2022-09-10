function start_auto_parse() {
    $.post('/api/service/start_auto_parse', {}, function (data) {
            let code = data['code'];
            if (code === 500) {
                alert('开始自动解析同步地址')
            } else {
                alert('已经在执行解析同步地址')
            }
        }
    )
}
function start_auto_search() {
    $.post('/api/service/start_auto_search', {}, function (data) {
            let code = data['code'];
            if (code === 500) {
                alert('开始自动搜索元数据')
            } else {
                alert('已经在执行自动搜索元数据')
            }
        }
    )
}
function start_auto_link() {
    $.post('/api/service/start_auto_link', {}, function (data) {
            let code = data['code'];
            if (code === 500) {
                alert('开始自动链接')
            } else {
                alert('已经在执行自动链接')
            }
        }
    )
}
function auto_parse_state() {
    $.post('/api/service/auto_parse_state', {}, function (data) {
            let results = data['results'];
            if (results === 1) {
                alert('已经在执行解析同步地址')
            } else {
                alert('未在执行解析同步地址')
            }
        }
    )
}
function auto_search_state() {
    $.post('/api/service/auto_search_state', {}, function (data) {
            let results = data['results'];
            if (results === 1) {
                alert('已经在执行自动搜索元数据')
            } else {
                alert('未在执行自动搜索元数据')
            }
        }
    )
}
function auto_link_state() {
    $.post('/api/service/auto_link_state', {}, function (data) {
            let results = data['results'];
            if (results === 1) {
                alert('已经在执行自动链接')
            } else {
                alert('未在执行自动链接')
            }
        }
    )
}
function bind() {
    $('#start_auto_parse').click(start_auto_parse)
    $('#start_auto_search').click(start_auto_search)
    $('#auto_parse_state').click(auto_parse_state)
    $('#auto_search_state').click(auto_search_state)
    $('#start_auto_link').click(start_auto_link)
    $('#auto_link_state').click(auto_link_state)
}

$(document).ready(bind)