let s:unite_source = {
\   'name': 'def',
\ }
function! s:unite_source.gather_candidates(args, context)
  let s:exePath ="YOUR_DICT/main.py"
  let s:path  = expand('%:p')
  let s:ext   = expand('%:e')
  let s:lines = getbufline('%', 1, '$')

  let s:func_list   = []
  let s:line_number = 1
  let argvs         = []

  for line in s:lines
    if line =~ 'def ' && s:ext == "py"
      let tmp       = substitute(line, "def ", "", "g")
      let lastIndex = match(tmp, "(")
      call add(argvs, strpart(tmp, 0, lastIndex))
    endif
    let s:line_number += 1
  endfor
  let s:result   = system('python '.s:exePath.' '.join(argvs, " "))
  let s:dataList = split(s:result, "||")
  for data in s:dataList
    let input = split(data, "++")
    call add(s:func_list, [input[0], input[1], str2nr(input[2])])
  endfor

  return map(copy(s:func_list), '{
  \   "word"        : v:val[0],
  \   "source"      : "get_function",
  \   "kind"        : "jump_list",
  \   "action__path": v:val[1],
  \   "action__line": v:val[2]
  \ }')

endfunction
call unite#define_source(s:unite_source)
unlet s:unite_source
