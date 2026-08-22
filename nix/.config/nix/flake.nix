{
  description = "Example nix-darwin system flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nix-darwin.url = "github:nix-darwin/nix-darwin/master";
    nix-darwin.inputs.nixpkgs.follows = "nixpkgs";
    nix-homebrew.url = "github:zhaofengli/nix-homebrew";
  };

  outputs = inputs@{ self, nix-darwin, nixpkgs , nix-homebrew }:
  let
    configuration = { pkgs, config, ... }: {

      system.primaryUser = "hexlo";
      
      nixpkgs.config.allowUnfree = true;
      
      # List packages installed in system profile. To search by name, run:
      # $ nix-env -qaP | grep wget
      environment.systemPackages =
        [ 
          pkgs.firefox
          pkgs.ghostty-bin
          pkgs.helix
          pkgs.mkalias
          pkgs.lazydocker
          pkgs.lazygit
          pkgs.starship
          pkgs.tmux
          pkgs.vim
          pkgs.zellij
        ];

      homebrew = {
        enable = true;
        brews = [
          "mas"
        ];
        casks = [
          "iina"
          "plex"
          "plexamp"
          "steam"
          "the-unarchiver"
        ];
        masApps = {
          "Infuse" = 1136220934;
        };
        onActivation = {
          cleanup = "zap";

          # Stops Homebrew from triggering a breaking 
          # self-update routine mid-activation.
          autoUpdate = false;
          upgrade = false;
        };
      };
      
      fonts.packages = with pkgs; [
        nerd-fonts.jetbrains-mono
      ];

      # Activation Script to create macOS alias instead of symlink for apps
      system.activationScripts.applications.text = let
        env = pkgs.buildEnv {
          name = "system-applications";
          paths = config.environment.systemPackages;
          pathsToLink = [ "/Applications" ];
        };
      in
        pkgs.lib.mkForce ''
        # Set up applications.
        echo "setting up /Applications..." >&2
        rm -rf /Applications/Nix\ Apps
        mkdir -p /Applications/Nix\ Apps
        find ${env}/Applications -maxdepth 1 -type l -exec readlink '{}' + |
        while read -r src; do
          app_name=$(basename "$src")
          echo "copying $src" >&2
          ${pkgs.mkalias}/bin/mkalias "$src" "/Applications/Nix Apps/$app_name"
        done
             '';

      system.defaults = {
        dock.autohide = true;
        dock.show-recents = false;
        dock.persistent-apps = [
          "${pkgs.ghostty-bin}/Applications/Ghostty.app"
          "${pkgs.firefox}/Applications/Firefox.app"
          "/Applications/IINA.app"
          "/Applications/Infuse.app"
          "/Applications/Plex.app"
          "/Applications/Plexamp.app"
          "/System/Applications/Mail.app"
          "/System/Applications/Calendar.app"
        ];
        finder.CreateDesktop = false;
        finder.FXPreferredViewStyle = "clmv";
        finder.NewWindowTarget = "Home";
        finder.ShowPathbar = true;
        finder.ShowStatusBar = true;
        loginwindow.GuestEnabled = false;
        NSGlobalDomain.AppleICUForce24HourTime = true;
        NSGlobalDomain.AppleInterfaceStyle = "Dark";
      };
      
      # Necessary for using flakes on this system.
      nix.settings.experimental-features = "nix-command flakes";

      # Enable alternative shell support in nix-darwin.
      # programs.fish.enable = true;

      # Set Git commit hash for darwin-version.
      system.configurationRevision = self.rev or self.dirtyRev or null;

      # Used for backwards compatibility, please read the changelog before changing.
      # $ darwin-rebuild changelog
      system.stateVersion = 6;

      # The platform the configuration will be used on.
      nixpkgs.hostPlatform = "aarch64-darwin";
    };
  in
  {
    # Build darwin flake using:
    # $ darwin-rebuild build --flake .#mbp
    darwinConfigurations."mbp" = nix-darwin.lib.darwinSystem {
      modules = [
        configuration
        nix-homebrew.darwinModules.nix-homebrew
        {
          nix-homebrew = {
            # Install Homebrew under the default prefix
            enable = true;

            # Apple Silicon Only: Also install Homebrew under the default Intel prefix for Rosetta 2
            enableRosetta = true;

            # User owning the Homebrew prefix
            user = "hexlo";

            autoMigrate = true;
          };
        }
      ];
    };
  };
}
