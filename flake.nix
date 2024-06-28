{
  description = "Extract constants from convolutional neural networks";

  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in {
        packages = {
          convconst = mkPoetryApplication {
            projectDir = self;
            preferWheels = true;
          };

          default = self.packages.${system}.convconst;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.convconst ];
          packages = [ pkgs.poetry ];
        };
      }
    );
}
