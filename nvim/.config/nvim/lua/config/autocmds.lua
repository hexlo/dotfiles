-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

-- After `:Lazy sync`/`:Lazy update`, force nvim-treesitter to recompile any
-- parsers whose bundled query files changed. Without this, a stale compiled
-- parser (e.g. vim.so) can go out of sync with an updated highlights.scm and
-- throw "Invalid node type" query errors (seen via noice.nvim) until the next
-- manual :TSUpdate.
vim.api.nvim_create_autocmd("User", {
  pattern = "LazySync",
  group = vim.api.nvim_create_augroup("auto_tsupdate_after_lazy_sync", { clear = true }),
  callback = function()
    if pcall(require, "nvim-treesitter") then
      vim.cmd("TSUpdate")
    end
  end,
})
