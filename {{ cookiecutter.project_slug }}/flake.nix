{
  description = "{{ cookiecutter.description }}";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/79d3ca08920364759c63fd3eb562e99c0c17044a";
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
        apps = {
          {{ cookiecutter.project_slug }} = pkgs.{{ cookiecutter.project_slug }};
        };

        defaultApp = pkgs.{{ cookiecutter.project_slug }};

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            postgresql
            nodejs-16_x
            (python310.withPackages (ps: with ps; [ poetry ]))
          ] ++ lib.optional stdenv.isDarwin openssl;
        };
      }));
}
