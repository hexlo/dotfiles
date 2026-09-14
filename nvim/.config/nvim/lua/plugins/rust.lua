return {
  {
    "mrcjkb/rustaceanvim",
    opts = {
      server = {
        default_settings = {
          ["rust-analyzer"] = {
            check = { command = "clippy" }, -- run `cargo clippy` on save, not just `cargo check`
          },
        },
      },
    },
  },
}
