require("nvim-treesitter.configs").setup({
  ensure_installed = {
    "c", "cpp", "python", "lua", "vim", "vimdoc", "bash", "markdown", "markdown_inline"
  },
  auto_install = true,
  highlight = {
    enable = true,
    additional_vim_regex_highlighting = {},
  },
  indent = {
    enable = true,
    disable = { "python" },
  },

  -- ----------------------------------------
  -- TEXT OBJECTS
  -- ----------------------------------------
  -- `move` is the main win in a large C++ codebase: ]m / [m step between
  -- function definitions and ]] / [[ between classes, which beats scrolling
  -- through thousand-line headers.
  --
  -- `select` deliberately avoids `af`/`if`: mini.ai already owns those for
  -- function *calls*, and the two-character map would shadow it. Functions
  -- are on `am`/`im` (m for method) instead. mini.ai keeps `a` (argument),
  -- `b` (brackets), `f` (call), `q` (quotes) and `t` (tag).
  textobjects = {
    select = {
      enable = true,
      lookahead = true, -- jump forward to the next object if not inside one
      keymaps = {
        ["am"] = "@function.outer",
        ["im"] = "@function.inner",
        ["ac"] = "@class.outer",
        ["ic"] = "@class.inner",
        ["al"] = "@loop.outer",
        ["il"] = "@loop.inner",
        ["ak"] = "@conditional.outer",
        ["ik"] = "@conditional.inner",
        ["a/"] = "@comment.outer",
      },
    },
    move = {
      enable = true,
      set_jumps = true, -- record jumps, so <C-o> walks back
      goto_next_start     = { ["]m"] = "@function.outer", ["]]"] = "@class.outer" },
      goto_next_end       = { ["]M"] = "@function.outer", ["]["] = "@class.outer" },
      goto_previous_start = { ["[m"] = "@function.outer", ["[["] = "@class.outer" },
      goto_previous_end   = { ["[M"] = "@function.outer", ["[]"] = "@class.outer" },
    },
    swap = {
      enable = true,
      swap_next     = { ["<leader>na"] = "@parameter.inner" },
      swap_previous = { ["<leader>pa"] = "@parameter.inner" },
    },
  },
})

-- .
