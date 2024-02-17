{
  description = "{{ cookiecutter.project_name }}";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryEnv mkPoetryApplication;
      in
      {
        packages = {
          {{ cookiecutter.project_slug }} = mkPoetryApplication { projectDir = self; };

          devEnv = mkPoetryEnv {
            projectDir = self;
            groups = [ "main" "dev" ];
          };

          # refresh venv for Pycharm with: nix build .#venv -o .venv
          venv = self.packages.${system}.devEnv;
          default = self.packages.${system}.{{ cookiecutter.project_slug }};
        };

        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            just
            poetry
            pre-commit
            self.packages.${system}.devEnv
          ];
        };
      });
}
