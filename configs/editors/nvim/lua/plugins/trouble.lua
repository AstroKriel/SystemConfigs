require("trouble").setup({
  focus = true, -- jump into the list when it opens, so it is navigable immediately
  warn_no_results = false,
  open_no_results = true, -- still open on a clean file, to confirm linting ran
})

-- ----------------------------------------
-- KEYBINDINGS
-- ----------------------------------------
-- <leader>x holds the diagnostics/list surface. The workspace picker is the
-- one that answers "is the linter actually finding anything", since clangd
-- only reports diagnostics for files it has opened and indexed.

local map = function(keys, cmd, desc)
  vim.keymap.set("n", keys, "<cmd>Trouble " .. cmd .. "<cr>", { desc = desc })
end

map("<leader>xx", "diagnostics toggle",                  "Diagnostics (workspace)")
map("<leader>xX", "diagnostics toggle filter.buf=0",     "Diagnostics (current buffer)")
map("<leader>xs", "symbols toggle win.position=right",   "Symbols outline")
map("<leader>xl", "loclist toggle",                      "Location list")
map("<leader>xq", "qflist toggle",                       "Quickfix list")

-- .
