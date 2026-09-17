local telescope = require("telescope")
local builtin = require("telescope.builtin")
local themes = require("telescope.themes")

-- ----------------------------------------
-- VENDORED CODE FILTERING
-- ----------------------------------------
-- Codebases like quokka carry their dependencies as submodules under extern/.
-- Submodules are tracked, so .gitignore does not hide them and they dominate
-- every search: in quokka, 86% of files and 85% of grep hits live in extern/.
-- The default pickers skip these directories; the shifted variants below
-- search them, for when a hunt genuinely leads down into a dependency.

local vendored = { "extern", "build" }

-- build an fd command, optionally including the vendored directories
local function fd_command(include_vendored)
  local cmd = { "fd", "--type", "f", "--hidden", "--exclude", ".git" }
  if not include_vendored then
    for _, dir in ipairs(vendored) do
      vim.list_extend(cmd, { "--exclude", dir })
    end
  end
  return cmd
end

-- build ripgrep glob args, optionally including the vendored directories
local function rg_globs(include_vendored)
  local args = {}
  if not include_vendored then
    for _, dir in ipairs(vendored) do
      table.insert(args, "--glob=!" .. dir .. "/**")
    end
  end
  return args
end

-- ----------------------------------------
-- SETUP
-- ----------------------------------------

telescope.setup({
  pickers = {
    find_files = {
      find_command = fd_command(false),
    },
    live_grep = {
      additional_args = function()
        return rg_globs(false)
      end,
    },
  },
  extensions = {
    ["ui-select"] = themes.get_dropdown(),
  },
})

-- load extensions
pcall(telescope.load_extension, "fzf")
pcall(telescope.load_extension, "ui-select")

-- ----------------------------------------
-- KEYBINDINGS
-- ----------------------------------------

vim.keymap.set("n", "<leader>sf", builtin.find_files, { desc = "[S]earch [F]iles" })
vim.keymap.set("n", "<leader>sg", builtin.live_grep,  { desc = "[S]earch by [G]rep" })
vim.keymap.set("n", "<leader>sb", builtin.buffers,    { desc = "[S]earch [B]uffers" })
vim.keymap.set("n", "<leader>sh", builtin.help_tags,  { desc = "[S]earch [H]elp" })
vim.keymap.set("n", "<leader>sk", builtin.keymaps,    { desc = "[S]earch [K]eymaps" })
vim.keymap.set("n", "<leader>sr", builtin.resume,     { desc = "[S]earch [R]esume" })
vim.keymap.set("n", "<leader>sd", builtin.diagnostics, { desc = "[S]earch [D]iagnostics" })

-- shifted variants: the same search, widened to include extern/ and build/
vim.keymap.set("n", "<leader>sF", function()
  builtin.find_files({
    find_command = fd_command(true),
    prompt_title = "Find Files (incl. vendored)",
  })
end, { desc = "[S]earch [F]iles (incl. vendored)" })

vim.keymap.set("n", "<leader>sG", function()
  builtin.live_grep({
    additional_args = function()
      return rg_globs(true)
    end,
    prompt_title = "Live Grep (incl. vendored)",
  })
end, { desc = "[S]earch by [G]rep (incl. vendored)" })

-- special case: fuzzy search in current buffer
vim.keymap.set("n", "<leader>/", function()
  builtin.current_buffer_fuzzy_find(themes.get_dropdown {
    winblend = 10,
    previewer = false,
  })
end, { desc = "[/] Search in current buffer" })

-- .
