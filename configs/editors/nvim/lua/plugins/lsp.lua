-- make all lsp floating windows use a rounded white border
local float_opts = { border = "rounded", max_width=80, focusable = false }
vim.lsp.handlers["textDocument/hover"] = vim.lsp.with(vim.lsp.handlers.hover, float_opts)
vim.lsp.handlers["textDocument/signatureHelp"] = vim.lsp.with(vim.lsp.handlers.signature_help, float_opts)
vim.api.nvim_set_hl(0, "NormalFloat",  { bg = "black" })
vim.api.nvim_set_hl(0, "FloatBorder", { fg = "white", bg = "black" })

-- create capabilities using standard nvim-cmp support
local capabilities = require("cmp_nvim_lsp").default_capabilities()

-- setup lsp-related keymaps and inlay hints when the lsp attaches
vim.api.nvim_create_autocmd("LspAttach", {
  group = vim.api.nvim_create_augroup("user-lsp-attach", { clear = true }),
  callback = function(event)
    local map = function(keys, func, desc, mode)
      vim.keymap.set(mode or "n", keys, func, { buffer = event.buf, desc = "LSP: " .. desc })
    end

    map("grn", vim.lsp.buf.rename, "[R]e[n]ame")
    map("gra", vim.lsp.buf.code_action, "[G]oto Code [A]ction", { "n", "x" })
    map("grr", require("telescope.builtin").lsp_references, "[G]oto [R]eferences")
    map("gri", require("telescope.builtin").lsp_implementations, "[G]oto [I]mplementation")
    map("grd", require("telescope.builtin").lsp_definitions, "[G]oto [D]efinition")
    map("grD", vim.lsp.buf.declaration, "[G]oto [D]eclaration")
    map("grt", require("telescope.builtin").lsp_type_definitions, "[G]oto [T]ype Definition")
    map("gO", require("telescope.builtin").lsp_document_symbols, "Open Document Symbols")
    map("gW", require("telescope.builtin").lsp_dynamic_workspace_symbols, "Open Workspace Symbols")
  end,
})

-- basic diagnostics configuration
vim.diagnostic.config({
  severity_sort = true,
  float = { border = "rounded", source = "if_many" },
  underline = true,
  virtual_text = {
    source = "if_many",
    spacing = 2,
  },
})

-- lsp server list (lspconfig names)
local servers = {
  pyright  = {}, -- python
  clangd   = {}, -- c++
  texlab   = {}, -- latex
  lua_ls   = {}, -- lua
  marksman = {}, -- markdown
  bashls   = {}, -- bash
}

-- mason package names, only where they differ from the lspconfig name above
local mason_name_overrides = {
  lua_ls = "lua-language-server",
  bashls = "bash-language-server",
}

local mason_package_names = {}
for server_name, _ in pairs(servers) do
  table.insert(mason_package_names, mason_name_overrides[server_name] or server_name)
end

-- ensure tools are installed
require("mason-tool-installer").setup({
  ensure_installed = mason_package_names,
})

-- apply the cmp capabilities to every server. mason-lspconfig v2 dropped the
-- `handlers` option it used to be passed through, so setting it there is
-- silently ignored; `vim.lsp.config("*", ...)` is the replacement.
vim.lsp.config("*", {
  capabilities = capabilities,
})

-- v2 enables every installed server itself via vim.lsp.enable()
require("mason-lspconfig").setup({})

-- vim.lsp.enable() attaches on FileType. A file named on the command line
-- (`nvim src/hydro/mhd_system.hpp`) has already fired FileType by the time the
-- servers are enabled, so nothing attaches and the buffer silently has no LSP.
-- Re-fire it once for buffers that are already loaded.
vim.schedule(function()
  for _, buf in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_loaded(buf) and vim.bo[buf].filetype ~= "" then
      vim.api.nvim_exec_autocmds("FileType", { buffer = buf, modeline = false })
    end
  end
end)

-- .