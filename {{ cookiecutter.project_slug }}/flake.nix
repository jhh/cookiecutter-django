{
  description = "{{ cookiecutter.description }}";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          # The application
          {{ cookiecutter.project_slug }} = prev.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
          };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      {

        packages.default = pkgs.{{ cookiecutter.project_slug }}.dependencyEnv;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            postgresql
            nodejs
            poetry
            pre-commit
          ] ++ lib.optional stdenv.isDarwin openssl;
        };
      }));
}
