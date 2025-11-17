{
  description = "Python + Arcade Dev Shell (no devenv)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            python
            python.pkgs.pip
            python.pkgs.virtualenv

            pkgs.cairo
            pkgs.pkg-config
            pkgs.libGL
            pkgs.libGLU
            pkgs.gdk-pixbuf
            pkgs.pango
            pkgs.gtk3
            pkgs.atk

            pkgs.SDL2
            pkgs.SDL2_image
            pkgs.SDL2_mixer
            pkgs.SDL2_ttf
          ];

          shellHook = ''
            # Only really need to do this for development, since my default shell isn't posix-compliant (Nushell)
            shell="${pkgs.bash}/bin/bash";

            SHELL="$shell"

            if [ ! -d .venv ]; then
              python3 -m venv .venv
            fi

            source .venv/bin/activate

            pip install --upgrade pip
            pip install arcade pillow pytest
          '';
        };
      });
}
