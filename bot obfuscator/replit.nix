{ pkgs }: {
    deps = [
        pkgs.python38Full
    ];
    env = {
        PYTHON_LD_LIBREARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            pkgs.glib
            pkgs.pkgs.xorg.libX11
        ];
        PYTHONBIN = "${pkgs.python38Full}/bin/python3.8";
        LANG = "ES_ES.UTF-8"
    }
}