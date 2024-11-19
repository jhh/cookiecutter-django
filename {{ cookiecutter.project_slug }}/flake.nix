{
  description = "{{ cookiecutter.project_name }}";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:adisbladis/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, uv2nix, pyproject-nix, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      wsgiApp = "config.wsgi:application";
      settingsModules = {
        prod = "config.settings";
      };

      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };

      # Python sets grouped per system
      pythonSets = forAllSystems
        (
          system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
            inherit (pkgs) stdenv;

            # Base Python package set from pyproject.nix
            baseSet = pkgs.callPackage pyproject-nix.build.packages {
              python = pkgs.python312;
            };

            # An overlay of build fixups & test additions
            pyprojectOverrides = final: prev: {

              # {{ cookiecutter.__project_snake }} is the name of our example package
              {{ cookiecutter.__project_snake }} = prev.{{ cookiecutter.__project_snake }}.overrideAttrs (old: {

              passthru = old.passthru // {
              tests =
              (old.tests or { }) //
              {

              mypy =
              let
              venv = final.mkVirtualEnv "{{ cookiecutter.__project_snake }}-typing-env" {
              {{ cookiecutter.__project_snake }} = [ "typing" ];
            };
          in
          stdenv.mkDerivation {
            name = "${final.{{ cookiecutter.__project_snake }}.name}-mypy";
            inherit (final.{{ cookiecutter.__project_snake }}) src;
            nativeBuildInputs = [ venv ];
            dontConfigure = true;
            dontInstall = true;
            buildPhase = ''
              export MYPYPATH=apps
              mypy . --junit-xml $out/junit.xml
            '';
          };

        pytest =
      let
      venv = final.mkVirtualEnv "{{ cookiecutter.__project_snake }}-pytest-env" {
      {{ cookiecutter.__project_snake }} = [ "test" ];
      };
      in
      stdenv.mkDerivation {
      name = "${final.{{ cookiecutter.__project_snake }}.name}-pytest";
      inherit (final.{{ cookiecutter.__project_snake }}) src;
      nativeBuildInputs = [
        venv
      ];

      dontConfigure = true;

      buildPhase = ''
        pytest --junit-xml=$out/junit.xml
      '';
      };
      } // lib.optionalAttrs stdenv.isLinux {
      #
      nixos =
        let
          venv = final.mkVirtualEnv "{{ cookiecutter.__project_snake }}-nixos-test-env" workspace.deps.default;
          secrets = pkgs.writeText "{{ cookiecutter.__project_snake }}-test-secrets" ''
            DEBUG=false
            DJANGO_DATABASE_URL="sqlite:///tmp/db.sqlite3"
          '';
        in
        pkgs.nixosTest {
          name = "{{ cookiecutter.__project_snake }}-nixos-test";

          nodes.machine = { ... }:
            {
              imports = [
                self.nixosModules.default
              ];

              services.{{ cookiecutter.__project_snake }} = {
                enable = true;
                inherit venv;
                secrets = [ secrets ];
              };

              system.stateVersion = "24.11";
            };

          testScript = ''
            with subtest("Check {{ cookiecutter.__project_snake }} app comes up"):
                machine.wait_for_unit("{{ cookiecutter.__project_snake }}.service")
                machine.wait_for_open_port(8000)

            with subtest("Staticfiles are generated"):
              machine.succeed("curl -sf http://localhost:8000/static/ui/main.css")
          '';
        };
      };
      };
      });

      };

      in
      baseSet.overrideScope (lib.composeExtensions overlay pyprojectOverrides)
      );

      # Django static roots grouped per system
      staticRoots = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          inherit (pkgs) stdenv;

          pythonSet = pythonSets.${system};

          venv = pythonSet.mkVirtualEnv "{{ cookiecutter.__project_snake }}-env" workspace.deps.default;

        in
        stdenv.mkDerivation {
          name = "{{ cookiecutter.__project_snake }}-static";
          inherit (pythonSet.{{ cookiecutter.__project_snake }}) src;

          dontConfigure = true;
          dontBuild = true;

          nativeBuildInputs = [
            venv
          ];

          installPhase = ''
            export DJANGO_STATIC_ROOT="$out"
            {{ cookiecutter.__project_snake }}-manage collectstatic
          '';
        }
      );

    in
    {
      checks = forAllSystems
        (
          system:
          let
            pythonSet = pythonSets.${system};
          in
          # Inherit tests from passthru.tests into flake checks
          pythonSet.{{ cookiecutter.__project_snake }}.passthru.tests
      );

      nixosModules = {
        default = { config, lib, pkgs, ... }:
          let
            cfg = config.services.{{ cookiecutter.__project_snake }};
            inherit (pkgs) system;

            pythonSet = pythonSets.${system};

            inherit (lib.options) mkOption;
            inherit (lib.modules) mkIf;
          in
          {
            options.services.{{ cookiecutter.__project_snake }} = {
              enable = mkOption {
                type = lib.types.bool;
                default = false;
                description = ''
                  Enable {{ cookiecutter.__project_snake }}
                '';
              };

              settings-module = mkOption {
                type = lib.types.string;
                default = settingsModules.prod;
                description = ''
                  Django settings module
                '';
              };

              venv = mkOption {
                type = lib.types.package;
                default = pythonSet.mkVirtualEnv "{{ cookiecutter.__project_snake }}-env" workspace.deps.default;
                description = ''
                  {{ cookiecutter.__project_snake }} virtual environment package
                '';
              };

              static-root = mkOption {
                type = lib.types.package;
                default = staticRoots.${system};
                description = ''
                  {{ cookiecutter.__project_snake }} static root
                '';
              };

              secrets = lib.mkOption {
                type = with lib.types; listOf path;
                description = ''
                  A list of files containing the various secrets. Should be in the format
                  expected by systemd's `EnvironmentFile` directory.
                '';
                default = [ ];
              };
            };

            config = mkIf cfg.enable {
              systemd.services.{{ cookiecutter.__project_snake }} = {
                description = "{{ cookiecutter.__project_snake }} server";

                environment = {
                  DJANGO_SETTINGS_MODULE = cfg.settings-module;
                  DJANGO_STATIC_ROOT = cfg.static-root;
                };

                serviceConfig = {
                  EnvironmentFile = cfg.secrets;
                  ExecStartPre = "${cfg.venv}/bin/{{ cookiecutter.__project_snake }}-manage migrate --no-input";
                  ExecStart = ''
                    ${cfg.venv}/bin/gunicorn ${wsgiApp}
                  '';
                  Restart = "on-failure";

                  DynamicUser = true;
                  StateDirectory = "{{ cookiecutter.__project_snake }}";
                  RuntimeDirectory = "{{ cookiecutter.__project_snake }}";

                  BindReadOnlyPaths = [
                    "${
                      config.environment.etc."ssl/certs/ca-certificates.crt".source
                    }:/etc/ssl/certs/ca-certificates.crt"
                    builtins.storeDir
                    "-/etc/resolv.conf"
                    "-/etc/nsswitch.conf"
                    "-/etc/hosts"
                    "-/etc/localtime"
                  ];

                  RestrictAddressFamilies = "AF_UNIX AF_INET";
                  CapabilityBoundingSet = "";
                  SystemCallFilter = [ "@system-service" "~@privileged @setuid @keyring" ];
                };

                wantedBy = [ "multi-user.target" ];
              };
            };

          };

      };

      packages = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonSet = pythonSets.${system};
        in
        {
          default =
            let
              venv = pythonSet.mkVirtualEnv "{{ cookiecutter.__project_snake }}-env" workspace.deps.default;
            in
            pkgs.writeShellApplication {
              name = "manage";
              text = ''
                if [ "$UID" -ne 0 ]; then
                    echo "error: run this command as root."
                    exit 1
                fi
                sudo -u {{ cookiecutter.__project_snake }} env DJANGO_DATABASE_URL=postgres:///{{ cookiecutter.__project_snake }} ${venv}/bin/{{ cookiecutter.__project_snake }}-manage "$@"
              '';
            };

          static = staticRoots.${system};
        } //
        lib.optionalAttrs pkgs.stdenv.isLinux {
          # Expose Docker container in packages
          docker =
            let
              venv = pythonSet.mkVirtualEnv "{{ cookiecutter.__project_snake }}-env" workspace.deps.default;
            in
            pkgs.dockerTools.buildLayeredImage {
              name = "{{ cookiecutter.__project_snake }}";
              contents = [ pkgs.cacert ];
              config = {
                Cmd = [
                  "${venv}/bin/gunicorn"
                  wsgiApp
                ];
                Env = [
                  "DJANGO_SETTINGS_MODULE=${settingsModules.prod}"
                  "DJANGO_STATIC_ROOT=${staticRoots.${system}}"
                ];
              };
            };
        }
      );

      apps = forAllSystems
        (
          system: {
            default = {
              type = "app";
              program = "${self.packages.${system}.default}/bin/manage";
            };
          }
        );

      # Use an editable Python set for development.
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          editablePythonSet = pythonSets.${system}.overrideScope editableOverlay;
          venv = editablePythonSet.mkVirtualEnv "{{ cookiecutter.__project_snake }}-dev-env" workspace.deps.all;
          packages = with pkgs; [
            just
            nodejs
            pre-commit
          ];
        in
        {
          impure = pkgs.mkShell {
            inherit packages;
          };

          default = pkgs.mkShell {
            packages = packages ++ [ venv ];
            shellHook = ''
              unset PYTHONPATH
              export REPO_ROOT=$(git rev-parse --show-toplevel)
              export UV_NO_SYNC=1
            '';
          };
        }
      );
    };
}
