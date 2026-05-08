#!/usr/bin/env bash
# =============================================================================
#   Termux Build Init
#   Auto create & build GitHub repo as a Termux .deb package
#   github.com/djunekz/termux-app-store
# =============================================================================
set -uo pipefail

_SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ "$(basename "$_SELF_DIR")" == "tools" ]]; then
    ROOT="$(dirname "$_SELF_DIR")"
else
    ROOT="$_SELF_DIR"
fi
PACKAGES_DIR="$ROOT/packages"
BUILD_SCRIPT="$ROOT/build-package.sh"

R=$'\033[0m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
GRAY=$'\033[90m'
WHITE=$'\033[97m'
GREEN=$'\033[32m'
BGREEN=$'\033[92m'
YELLOW=$'\033[33m'
BYELLOW=$'\033[93m'
CYAN=$'\033[36m'
BCYAN=$'\033[96m'
BRED=$'\033[91m'
BG_RED=$'\033[41m'
BLACK=$'\033[30m'

N="$R"; G="$BGREEN"; Y="$BYELLOW"; B="$BCYAN"; C="$BCYAN"; W="$WHITE"
ok()    { printf "${BGREEN}[${GREEN}✓${BGREEN}]${R}  %s\n" "$*"; }
info()  { printf "${BGREEN}[${BCYAN}INFO${BGREEN}]${R}  %s\n" "$*"; }
warn()  { printf "${BGREEN}[${BYELLOW}!${BGREEN}]${R}  %s\n" "$*"; }
fail()  { printf "${BGREEN}[${BRED}FAIL${BGREEN}]${R}  %s\n" "$*"; exit 1; }
detail(){ printf "     ${GRAY}%-14s${R} ${DIM}%s${R}\n" "$1" "$2"; }
step()  { echo ""; printf "${BYELLOW}— %s —${R}\n" "$*"; }

banner() {
  local _w; _w=$(tput cols 2>/dev/null || echo 72)
  local _l; _l=$(printf '%.0s─' $(seq 1 $_w))
  echo ""
  printf "${BCYAN}${_l}${R}\n"
  printf "${BOLD}${BCYAN}"
  printf "%*s" $(( (_w + 18) / 2 )) "Termux Build Init"
  printf "${R}\n"
  printf "${GRAY}"
  printf "%*s" $(( (_w + 36) / 2 )) "github.com/djunekz/termux-app-store"
  printf "${R}\n"
  printf "${GRAY}"
  printf "%*s" $(( (_w + 50) / 2 )) "Supports: GitHub · GitLab · Codeberg · Direct URL"
  printf "${R}\n"
  printf "${BCYAN}${_l}${R}\n"
  echo ""
}

need() {
    command -v "$1" &>/dev/null || fail "Required tool not found: $1 — install it first"
}
need curl; need tar; need sha256sum; need sed; need awk

sanitize_pkgname() {
    local raw="$1"
    local name
    name=$(echo "$raw" | tr '[:upper:]' '[:lower:]')
    name=$(echo "$name" | tr '_' '-')
    name=$(echo "$name" | sed 's/[^a-z0-9-]/-/g')
    name=$(echo "$name" | sed 's/-\+/-/g')
    name="${name#-}"; name="${name%-}"
    echo "$name"
}

join_deps() {
    echo "$*" | tr ',' ' ' | tr ' ' '\n' | grep -v '^$' | sort -u \
        | awk 'BEGIN{first=1} {if(first){printf "%s",$0;first=0} else {printf ", %s",$0}} END{print ""}'
}

pkg_deps() {
    echo "$*" | tr ' ' '\n' | grep '^pkg:' | sed 's/^pkg://' | sort -u | xargs
}

pip_deps() {
    echo "$*" | tr ' ' '\n' | grep '^pip:' | sed 's/^pip://' | sort -u | xargs
}

map_python_dep() {
    local mod="$1"
    case "$mod" in
        sys|os|re|io|abc|ast|cmd|csv|dis|gc|getopt|glob|gzip|hmac|http|ipaddress|\
        json|logging|math|mmap|operator|pathlib|pickle|platform|pprint|queue|\
        random|shlex|shutil|signal|socket|sqlite3|ssl|stat|string|struct|\
        subprocess|tempfile|textwrap|threading|time|traceback|typing|unicodedata|\
        unittest|urllib|uuid|warnings|xml|xmlrpc|zipfile|zlib|argparse|\
        collections|contextlib|copy|dataclasses|datetime|decimal|email|\
        enum|functools|hashlib|html|inspect|itertools|multiprocessing|\
        base64|binascii|builtins|cgi|cgitb|chunk|cmath|code|codecs|\
        compileall|concurrent|configparser|ctypes|curses|dbm|difflib|\
        doctest|encodings|filecmp|fileinput|fnmatch|fractions|ftplib|\
        getpass|gettext|grp|imaplib|importlib|keyword|lib2to3|linecache|\
        locale|lzma|mailbox|mailcap|marshal|mimetypes|modulefinder|\
        netrc|nis|nntplib|numbers|opcode|optparse|ossaudiodev|parser|\
        pdb|pkgutil|poplib|posix|posixpath|pprint|profile|pstats|pty|\
        pwd|py_compile|pyclbr|pydoc|readline|reprlib|resource|rlcompleter|\
        runpy|sched|secrets|select|selectors|shelve|smtpd|smtplib|\
        sndhdr|spwd|statistics|stringprep|sunau|symtable|sysconfig|\
        syslog|tabnanny|tarfile|telnetlib|termios|test|timeit|token|\
        tokenize|trace|tracemalloc|tty|turtle|turtledemo|types|uu|venv|\
        wave|weakref|webbrowser|wsgiref|xdrlib|zipapp|zipimport|\
        urllib2|httplib|httplib2|urlparse|cookielib|Cookie|\
        ConfigParser|HTMLParser|Queue|StringIO|BytesIO|\
        BaseHTTPServer|SimpleHTTPServer|SocketServer|socketserver|\
        xmlrpclib|repr|sets|UserDict|UserList|UserString|\
        commands|exceptions|__future__|__builtin__|xmllib) return ;;
    esac

    case "$mod" in
        python)         echo "pkg:python" ;;
        rust)           echo "pkg:rust" ;;
        nodejs)         echo "pkg:nodejs" ;;
        nmap)           echo "pkg:nmap" ;;
        openssh)        echo "pkg:openssh" ;;
        gi)             echo "pkg:glib" ;;
        gzip)           echo "pkg:gzip" ;;
        zip)            echo "pkg:zip" ;;
        unzip)          echo "pkg:unzip" ;;
        git)            echo "pkg:git" ;;
        bzip2)          echo "pkg:bzip2" ;;
        xz)             echo "pkg:xz" ;;
        clang)          echo "pkg:clang" ;;
        cmake)          echo "pkg:cmake" ;;
        libtool)        echo "pkg:libtool" ;;
        ninja)          echo "pkg:ninja" ;;
        automake)       echo "pkg:automake" ;;
        autoconf)       echo "pkg:autoconf" ;;
        python-setuptools) echo "pkg:python-setuptools" ;;
        python-wheel)   echo "pkg:python-wheel" ;;
        python-psutil)  echo "pkg:python-psutil" ;;
        python-pip)     echo "pkg:python-pip" ;;
        openssl)        echo "pkg:openssl" ;;
        openssl-dev)    echo "pkg:openssl-dev" ;;
        libffi)         echo "pkg:libffi" ;;
        zlib)           echo "pkg:zlib" ;;
        libffi-dev)     echo "pkg:libffi-dev" ;;
        zlib-dev)       echo "pkg:zlib-dev" ;;
        libxml2)        echo "pkg:libxml2" ;;
        libxml2-dev)    echo "pkg:libxml2-dev" ;;
        libjpeg-turbo)  echo "pkg:libjpeg-turbo" ;;
        libpng)         echo "pkg:libpng" ;;
        freetype)       echo "pkg:freetype" ;;
        sqlite)         echo "pkg:sqlite" ;;
        sqlite-dev)     echo "pkg:sqlite-dev" ;;
        libcurl)        echo "pkg:libcurl" ;;
        npm)            echo "pkg:npm" ;;
        perl)           echo "pkg:perl" ;;
        ruby)           echo "pkg:ruby" ;;
        gh)             echo "pkg:gh" ;;
        vim)            echo "pkg:vim" ;;
        tree)           echo "pkg:tree" ;;
        neovim)         echo "pkg:neovim" ;;
        hydra)          echo "pkg:hydra" ;;
        php)            echo "pkg:php" ;;
        libssh)         echo "pkg:libssh" ;;
        libssh2)        echo "pkg:libssh2" ;;
        mariadb)        echo "pkg:mariadb" ;;
        redis)          echo "pkg:redis" ;;
        imagemagick)    echo "pkg:imagemagick" ;;
        ffmpeg)         echo "pkg:ffmpeg" ;;
        termux-tools)   echo "pkg:termux-tools" ;;

        requests)       echo "pip:requests" ;;
        rich)           echo "pip:rich" ;;
        textual)        echo "pip:textual" ;;
        lxml)           echo "pip:lxml" ;;
        PIL|Pillow)     echo "pip:pillow" ;;
        numpy)          echo "pip:numpy" ;;
        pandas)         echo "pip:pandas" ;;
        scipy)          echo "pip:scipy" ;;
        matplotlib)     echo "pip:matplotlib" ;;
        cryptography)   echo "pip:cryptography" ;;
        paramiko)       echo "pip:paramiko" ;;
        scapy)          echo "pip:scapy" ;;
        psutil)         echo "pip:psutil" ;;
        pexpect)        echo "pip:pexpect" ;;
        ptyprocess)     echo "pip:ptyprocess" ;;
        asyncio|bisect|heapq|array|queue|abc|io|typing_extensions) return ;;
        tomllib|toml) return ;;

        yaml|ruamel)              echo "pip:PyYAML" ;;
        cv2)                      echo "pip:opencv-python" ;;
        PIL|Pillow)               echo "pip:Pillow" ;;
        sklearn)                  echo "pip:scikit-learn" ;;
        skimage)                  echo "pip:scikit-image" ;;
        bs4|beautifulsoup4)       echo "pip:beautifulsoup4" ;;
        dotenv)                   echo "pip:python-dotenv" ;;
        dateutil)                 echo "pip:python-dateutil" ;;
        jwt)                      echo "pip:PyJWT" ;;
        nacl)                     echo "pip:pynacl" ;;
        pyzmq|zmq)                echo "pip:pyzmq" ;;
        attr|attrs)               echo "pip:attrs" ;;
        charset_normalizer|chardet) echo "pip:chardet" ;;
        flask_restful)            echo "pip:flask-restful" ;;
        xdg_base_dirs|xdg)        echo "pip:xdg-base-dirs" ;;
        click_default_group)      echo "pip:click-default-group" ;;
        sqlmodel)                 echo "pip:sqlmodel" ;;
        tiktoken)                 echo "pip:tiktoken" ;;
        humanize)                 echo "pip:humanize" ;;
        textual)                  echo "pip:textual" ;;

        dnspython)      echo "pip:dnspyhton" ;;
        dnslib)         echo "pip:dnslib" ;;
        six)            echo "pip:six" ;;
        certifi)        echo "pip:certifi" ;;
        idna)           echo "pip:idna" ;;
        urllib3)        echo "pip:urllib3" ;;
        requests)       echo "pip:requests" ;;
        aiohttp)        echo "pip:aiohttp" ;;
        click)          echo "pip:click" ;;
        rich)           echo "pip:rich" ;;
        colorama)       echo "pip:colorama" ;;
        tzdata)         echo "pip:tzdata" ;;
        bcrypt)         echo "pip:bcrypt" ;;
        flask)          echo "pip:flask" ;;
        sqlalchemy)     echo "pip:sqlalchemy" ;;
        pydantic)       echo "pip:pydantic" ;;
        lxml)           echo "pip:lxml" ;;
        numpy)          echo "pip:numpy" ;;
        pandas)         echo "pip:pandas" ;;
        scipy)          echo "pip:scipy" ;;
        matplotlib)     echo "pip:matplotlib" ;;
        cryptography)   echo "pip:cryptography" ;;
        paramiko)       echo "pip:paramiko" ;;
        scapy)          echo "pip:scapy" ;;
        psutil)         echo "pip:psutil" ;;
        pexpect)        echo "pip:pexpect" ;;
        ptyprocess)     echo "pip:ptyprocess" ;;
        pyfiglet)       echo "pip:pyfiglet" ;;
        tqdm)           echo "pip:tqdm" ;;
        termcolor)      echo "pip:termcolor" ;;
        humanfriendly)  echo "pip:humanfriendly" ;;
        wget)           echo "pip:wget" ;;
        prettytable)    echo "pip:prettytable" ;;
        tabulate)       echo "pip:tabulate" ;;
        termtables)     echo "pip:termtables" ;;
        fire)           echo "pip:fire" ;;
        docopt)         echo "pip:docopt" ;;
        cachetools)     echo "pip:cachetools" ;;
        transformer)    echo "pip:transformer" ;;
        jinja2)         echo "pip:jinja2" ;;
        pytz)           echo "pip:pytz" ;;
        httpx)          echo "pip:httpx" ;;
        websockets)     echo "pip:websockets" ;;
        pynput)         echo "pip:pynput" ;;
        keyboard)       echo "pip:keyboard" ;;
        loguru)         echo "pip:loguru" ;;
        typer)          echo "pip:typer" ;;
        uvicorn)        echo "pip:uvicorn" ;;
        fastapi)        echo "pip:fastapi" ;;
        django)         echo "pip:django" ;;
        pyperclip)      echo "pip:pyperclip" ;;
        netifaces)      echo "pip:netifaces" ;;
        netaddr)        echo "pip:netaddr" ;;

        *)              echo "pip:$mod" ;;
    esac
}

scan_python_declared_deps() {
    local src="$1"
    local deps=()

    if [[ -f "$src/requirements.txt" ]]; then
        while IFS= read -r line; do
            [[ -z "$line" || "$line" == \#* ]] && continue
            [[ "$line" =~ ^[[:space:]]*- ]] && continue
            line=$(echo "$line" | sed 's/[>=<!~^].*//' | tr -d ' ' | cut -d'[' -f1)
            [[ -z "$line" ]] && continue
            local mapped; mapped=$(map_python_dep "$line")
            [[ -n "$mapped" ]] && deps+=("$mapped")
        done < "$src/requirements.txt"
    fi

    if [[ -f "$src/setup.py" ]]; then
        local reqs
        reqs=$(sed -n '/install_requires/,/\]/p' "$src/setup.py" 2>/dev/null \
            | grep -o '"[^"]*"\|'\''[^'\'']*'\''' \
            | tr -d '"'\''  ' \
            | sed 's/[>=<!~^].*//' || true)
        while IFS= read -r line; do
            [[ -z "$line" ]] && continue
            local mapped; mapped=$(map_python_dep "$line")
            [[ -n "$mapped" ]] && deps+=("$mapped")
        done <<< "$reqs"
    fi

    if [[ -f "$src/pyproject.toml" ]]; then
        local reqs
        reqs=$(sed -n '/dependencies/,/\]/p' "$src/pyproject.toml" 2>/dev/null \
            | grep -o '"[^"]*"' \
            | tr -d '"' \
            | sed 's/[>=<!~^;\[].*//' || true)
        for mod in $reqs; do
            [[ -z "$mod" ]] && continue
            local mapped; mapped=$(map_python_dep "$mod")
            [[ -n "$mapped" ]] && deps+=("$mapped")
        done
    fi

    [[ ${#deps[@]} -eq 0 ]] && echo "" && return
    printf '%s\n' "${deps[@]}" | sort -u | xargs
}

scan_python_imports() {
    local src="$1"
    local deps=()

    local pyfiles
    mapfile -t pyfiles < <(find "$src" -maxdepth 3 -name "*.py" 2>/dev/null)
    [[ ${#pyfiles[@]} -eq 0 ]] && echo "" && return

    local local_names
    local_names=$(find "$src" -maxdepth 2 \( -name "*.py" -o -type d \) 2>/dev/null \
        | xargs -I{} basename {} 2>/dev/null \
        | sed 's/\.py$//' | sort -u | tr '\n' '|' | sed 's/|$//')

    local imports
    imports=$(cat "${pyfiles[@]}" 2>/dev/null \
        | tr -d '\000' \
        | sed -n 's/^import  *\([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/p;
                   s/^from  *\([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/p' \
        | sort -u || true)

    for mod in $imports; do
        if [[ -n "$local_names" ]] && echo "$mod" | grep -qE "^(${local_names})$"; then
            continue
        fi
        local mapped; mapped=$(map_python_dep "$mod")
        [[ -n "$mapped" ]] && deps+=("$mapped")
    done

    [[ ${#deps[@]} -eq 0 ]] && echo "" && return
    printf '%s\n' "${deps[@]}" | sort -u | xargs
}

scan_shell_deps() {
    local src="$1"
    local deps=()
    local shfiles=()

    mapfile -t _sh < <(find "$src" -maxdepth 3 -name "*.sh" 2>/dev/null)
    shfiles+=("${_sh[@]}")

    while IFS= read -r _f; do
        grep -qU $'\x00' "$_f" 2>/dev/null && continue
        local _shebang
        _shebang=$(head -n1 "$_f" 2>/dev/null || true)
        echo "$_shebang" | grep -qE '^#!.*(bash|sh)\b' && shfiles+=("$_f")
    done < <(find "$src" -maxdepth 3 -type f ! -name "*.*" 2>/dev/null)

    [[ ${#shfiles[@]} -eq 0 ]] && echo "" && return

    local cmds _safe_shfiles=()
    for _sf in "${shfiles[@]}"; do
        grep -qU $'\x00' "$_sf" 2>/dev/null || _safe_shfiles+=("$_sf")
    done
    [[ ${#_safe_shfiles[@]} -eq 0 ]] && echo "" && return
    cmds=$(cat "${_safe_shfiles[@]}" 2>/dev/null \
        | tr -d '\000' \
        | sed -n \
            's/.*command -v  *\([a-zA-Z0-9_-]*\).*/\1/p;
             s/.*which  *\([a-zA-Z0-9_-]*\).*/\1/p;
             s/.*require  *\([a-zA-Z0-9_-]*\).*/\1/p;
             s/^[[:space:]]*\([a-zA-Z0-9_-]*\)[[:space:]].*/\1/p' \
        | grep -v '^$' | sort -u || true)
    for cmd in $cmds; do
        local mapped; mapped=$(map_shell_dep "$cmd")
        [[ -n "$mapped" ]] && deps+=("$mapped")
    done
    [[ ${#deps[@]} -eq 0 ]] && echo "" && return
    printf '%s\n' "${deps[@]}" | sort -u | xargs
}

map_shell_dep() {
    local cmd="$1"
    case "$cmd" in
        bash|sh|echo|printf|read|exit|source|cd|ls|cp|mv|rm|mkdir|cat|\
        grep|sed|awk|cut|tr|sort|uniq|head|tail|find|xargs|test|\
        true|false|export|local|return) return ;;
    esac
    case "$cmd" in
        iptables|ip6tables|ebtables|nftables) echo "warn:$cmd-requires-root-kernel-access-not-available-on-Termux" ;;
        hostapd|hostapd_cli)                  echo "warn:$cmd-requires-WiFi-AP-mode-not-available-on-Termux" ;;
        isc-dhcp-server|dhcpd|dnsmasq-dhcp)  echo "warn:$cmd-not-available-on-Termux" ;;
        systemctl|service|initctl)            echo "warn:$cmd-requires-systemd-not-available-on-Termux" ;;
        ifconfig|iwconfig|iwlist|iw)          echo "warn:$cmd-requires-root-network-access-not-available-on-Termux" ;;
        airmon-ng|airodump-ng|aireplay-ng|\
        aircrack-ng|airtun-ng)               echo "warn:$cmd-requires-monitor-mode-WiFi-not-available-on-Termux" ;;
        rfkill|wpa_supplicant|wpa_cli)        echo "warn:$cmd-requires-root-WiFi-access-not-available-on-Termux" ;;
        mount|umount|modprobe|insmod|rmmod)   echo "warn:$cmd-requires-root-kernel-access-not-available-on-Termux" ;;
        apt|apt-get|dpkg-reconfigure|yum|\
        pacman|dnf|zypper)                    echo "warn:$cmd-is-a-Linux-package-manager-use-pkg-on-Termux" ;;
        python3|python)  echo "pkg:python" ;;
        php)             echo "pkg:php" ;;
        ruby)            echo "pkg:ruby" ;;
        perl)            echo "pkg:perl" ;;
        node|nodejs)     echo "pkg:nodejs" ;;
        git)             echo "pkg:git" ;;
        curl)            echo "pkg:curl" ;;
        wget)            echo "pkg:wget" ;;
        nmap)            echo "pkg:nmap" ;;
        ssh|sshd)        echo "pkg:openssh" ;;
        zip)             echo "pkg:zip" ;;
        unzip)           echo "pkg:unzip" ;;
        openssl)         echo "pkg:openssl" ;;
        ffmpeg)          echo "pkg:ffmpeg" ;;
        convert|magick)  echo "pkg:imagemagick" ;;
        jq)              echo "pkg:jq" ;;
        dialog)          echo "pkg:dialog" ;;
        figlet|toilet)   echo "pkg:figlet" ;;
        whiptail)        echo "pkg:newt" ;;
        zenity|xterm|xdotool|xdpyinfo) echo "warn:$cmd-requires-X11-not-available-on-Termux" ;;
        *)               echo "" ;;
    esac
}

map_perl_dep() {
    local mod="$1"
    case "$mod" in
        strict|warnings|Exporter|Carp|Data::Dumper|File::Basename|File::Path|\
        File::Spec|File::Find|File::Temp|File::Copy|Cwd|Getopt::Long|\
        Getopt::Std|POSIX|Scalar::Util|List::Util|Storable|Encode|\
        Time::HiRes|Time::Local|MIME::Base64|Digest::MD5|Digest::SHA|\
        IO::File|IO::Handle|IO::Socket|IO::Select|Socket|Fcntl|\
        Config|constant|base|parent|vars|overload|utf8|feature|\
        B|Tie::Hash|Tie::Array|Tie::Scalar) return ;;

        Win32|Win32::*|WinAPI::*) return ;;

        HTTP::Request|HTTP::Response|HTTP::Headers|\
        LWP::UserAgent|LWP::Simple|LWP|WWW::Mechanize)
            echo "pkg:libwww-perl" ;;
        HTTP::Tiny)
            echo "pkg:perl" ;;
        URI|URI::*)
            echo "pkg:perl-uri" ;;
        HTML::Parser|HTML::TreeBuilder|HTML::Form|\
        HTML::Entities|HTML::Tagset)
            echo "pkg:perl-html-parser" ;;
        XML::Parser|XML::Simple|XML::LibXML)
            echo "pkg:perl-xml-parser" ;;
        DBI|DBD::*)
            echo "pkg:perl-dbi" ;;
        JSON|JSON::XS|JSON::PP|JSON::MaybeXS)
            echo "pkg:perl-json" ;;
        YAML|YAML::XS|YAML::Tiny)
            echo "pkg:perl-yaml" ;;
        Crypt::SSLeay|Net::SSLeay|IO::Socket::SSL)
            echo "pkg:perl-io-socket-ssl" ;;
        Digest::SHA1)
            echo "pkg:perl-digest-sha1" ;;
        Net::DNS)
            echo "pkg:perl-net-dns" ;;
        Net::Whois::IP|Net::Whois::Raw)
            echo "pkg:perl-net-whois-raw" ;;
        Net::Ping)
            echo "pkg:perl" ;;
        Term::ANSIColor|Term::ReadLine|Term::ReadKey)
            echo "pkg:perl-term-readkey" ;;
        Encode::*)
            echo "pkg:perl" ;;
        threads|Thread::*)
            echo "pkg:perl" ;;
        *)
            local cpan_name
            cpan_name=$(echo "$mod" | tr '::' '-' | tr '[:upper:]' '[:lower:]')
            echo "cpan:$mod" ;;
    esac
}

scan_perl_deps() {
    local src="$1"
    local deps=()
    local cpan_deps=()

    local plfiles
    mapfile -t plfiles < <(find "$src" -maxdepth 3 \( -name "*.pl" -o -name "*.pm" \) 2>/dev/null)
    [[ ${#plfiles[@]} -eq 0 ]] && echo "" && return

    local modules
    modules=$(cat "${plfiles[@]}" 2>/dev/null \
        | tr -d '\000' \
        | grep -E '^[[:space:]]*(use|require)[[:space:]]+' \
        | sed -n \
            "s/^[[:space:]]*use[[:space:]]\+\([A-Za-z][A-Za-z0-9:_]*\).*/\1/p;
             s/^[[:space:]]*require[[:space:]]\+['\"]\\?\([A-Za-z][A-Za-z0-9:_]*\)['\"]\\?.*/\1/p" \
        | grep -v '^[0-9]' \
        | sort -u || true)

    for mod in $modules; do
        local mapped; mapped=$(map_perl_dep "$mod")
        [[ -z "$mapped" ]] && continue
        if [[ "$mapped" == cpan:* ]]; then
            cpan_deps+=("${mapped#cpan:}")
        else
            deps+=("$mapped")
        fi
    done

    [[ ${#cpan_deps[@]} -gt 0 ]] && \
        printf '%s\n' "${cpan_deps[@]}" | sort -u | xargs | \
        sed 's/^/cpan: /' >&2 || true

    [[ ${#deps[@]} -eq 0 ]] && echo "" && return
    printf '%s\n' "${deps[@]}" | sort -u | xargs
}

detect_python_version() {
    local src="$1"
    local main="$2"

    local shebang=""
    grep -qU $'\x00' "$src/$main" 2>/dev/null || shebang=$(head -n1 "$src/$main" 2>/dev/null || true)
    if echo "$shebang" | grep -qE 'python2|python2\.[0-9]'; then
        echo "2"; return
    fi

    local pyfiles
    mapfile -t pyfiles < <(find "$src" -maxdepth 2 -name "*.py" 2>/dev/null)
    if [[ ${#pyfiles[@]} -gt 0 ]]; then
        if grep -lE '^[[:space:]]*print [^(]' "${pyfiles[@]}" 2>/dev/null | grep -q .; then
            echo "2"; return
        fi
        if grep -hE '^import (urllib2|httplib|ConfigParser|urlparse|cookielib)' \
                "${pyfiles[@]}" 2>/dev/null | grep -q .; then
            echo "2"; return
        fi
    fi

    echo "3"
}

detect_installer() {
    local src="$1"
    for candidate in install_Termux.sh install_termux.sh Install_Termux.sh setup_termux.sh install.sh Install.sh setup.sh Setup.sh; do
        [[ -f "$src/$candidate" ]] && echo "$candidate" && return
    done
    echo ""
}

detect_method() {
    local src="$1"
    if   [[ -f "$src/Cargo.toml" ]];     then echo "cargo"
    elif [[ -f "$src/go.mod" ]];          then echo "go"
    elif [[ -f "$src/package.json" ]];    then echo "npm"
    elif [[ -f "$src/CMakeLists.txt" ]];  then echo "cmake"
    elif [[ -f "$src/configure" || -f "$src/configure.ac" ]]; then echo "autotools"
    elif [[ -f "$src/setup.py" || -f "$src/pyproject.toml" ]]; then echo "pip"
    elif [[ -f "$src/Makefile" || -f "$src/makefile" ]]; then echo "make"
    elif ls "$src"/*.py &>/dev/null 2>&1; then echo "python-script"
    elif ls "$src"/*.pl &>/dev/null 2>&1; then echo "perl"
    elif ls "$src"/*.rb &>/dev/null 2>&1; then echo "ruby"
    elif ls "$src"/*.sh &>/dev/null 2>&1; then echo "shell"
    elif ls "$src"/*.lua &>/dev/null 2>&1; then echo "lua"
    elif ls "$src"/*.go &>/dev/null 2>&1; then echo "go"
    elif ls "$src"/*.php &>/dev/null 2>&1; then echo "php"
    elif ls "$src"/*.java &>/dev/null 2>&1; then echo "java"
    elif ls "$src"/*.kt &>/dev/null 2>&1;  then echo "kotlin"
    elif ls "$src"/*.swift &>/dev/null 2>&1; then echo "swift"
    elif ls "$src"/*.c "$src"/*.cpp &>/dev/null 2>&1; then echo "make"
    elif find "$src" -maxdepth 1 -type f ! -name "*.*" -perm /111 2>/dev/null | \
         xargs -I{} sh -c 'grep -qU $'"'"'\x00'"'"' "$1" 2>/dev/null || head -n1 "$1" 2>/dev/null' _ {} | grep -qE '^#!.*(bash|sh)\b'; then echo "shell"
    elif find "$src" -maxdepth 1 -type f ! -name "*.*" 2>/dev/null | \
         xargs -I{} sh -c 'grep -qU $'"'"'\x00'"'"' "$1" 2>/dev/null || head -n1 "$1" 2>/dev/null' _ {} | grep -qE '^#!.*(bash|sh)\b'; then echo "shell"
    else echo "unknown"
    fi
}

detect_entrypoint() {
    local src="$1"
    local pkg="$2"
    local method="${3:-}"
    local f

    if [[ "$method" == "python-script" || "$method" == "pip" ]]; then
        [[ -f "$src/$pkg.py" ]] && { echo "$pkg.py"; return; }
        f=$(grep -rl '__main__' "$src"/*.py 2>/dev/null \
            | grep -vi 'setup\|test\|conf' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
        f=$(grep -rl 'argparse\|optparse\|click\.command\|sys\.argv' "$src"/*.py 2>/dev/null \
            | grep -vi 'setup\|test\|conf' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
        f=$(ls "$src"/*.py 2>/dev/null \
            | grep -viE 'setup|conf|config|test|helper|util|__init__' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
    fi

    if [[ "$method" == "perl" ]]; then
        [[ -f "$src/$pkg.pl" ]] && { echo "$pkg.pl"; return; }
        f=$(ls "$src"/*.pl 2>/dev/null \
            | grep -viE 'install|setup|update|config|test|helper' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
    fi

    if [[ "$method" == "shell" ]]; then
        [[ -f "$src/$pkg"    ]] && { echo "$pkg";    return; }
        [[ -f "$src/$pkg.sh" ]] && { echo "$pkg.sh"; return; }
        f=$(ls "$src"/*.sh 2>/dev/null \
            | grep -viE 'setup|install|config|test|uninstall|update' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
    fi

    if [[ "$method" == "php" ]]; then
        [[ -f "$src/$pkg.php" ]] && { echo "$pkg.php"; return; }
        f=$(ls "$src"/*.php 2>/dev/null \
            | grep -viE 'config|conf|var|function|helper|class|Dockerfile' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
    fi

    if [[ "$method" == "go" ]]; then
        echo "$pkg"; return
    fi

    if [[ "$method" == "cargo" ]]; then
        local _cargo_name
        _cargo_name=$(grep -m1 '^name' "$src/Cargo.toml" 2>/dev/null \
            | sed 's/.*=.*"\(.*\)".*/\1/' || true)
        echo "${_cargo_name:-$pkg}"; return
    fi

    if [[ "$method" == "make" || "$method" == "autotools" || "$method" == "cmake" ]]; then

        if [[ -f "$src/$pkg.c" || -f "$src/$pkg.cpp" ]]; then
            echo "$pkg"; return
        fi

        if [[ -f "$src/CMakeLists.txt" ]]; then
            local _cmake_bin
            _cmake_bin=$(grep -m1 'add_executable' "$src/CMakeLists.txt" 2>/dev/null \
                | sed 's/.*add_executable[[:space:]]*([[:space:]]*\([^ )]*\).*/\1/' || true)
            [[ -n "$_cmake_bin" && "$_cmake_bin" != "\${" ]] && { echo "$_cmake_bin"; return; }
        fi

        if [[ -f "$src/configure.ac" || -f "$src/configure.in" ]]; then
            local _ac_name
            _ac_name=$(grep -m1 'AC_INIT' "${src}/configure.ac" "${src}/configure.in" 2>/dev/null \
                | sed 's/.*AC_INIT[[:space:]]*(\[*\([^]],)]*\).*/\1/' \
                | tr -d '[] \t' || true)
            if echo "$_ac_name" | grep -qE 'm4_|defn|\$|\(|\)|@'; then
                _ac_name=""
            fi
            [[ -n "$_ac_name" && "$_ac_name" != "AC_INIT" ]] && { sanitize_pkgname "$_ac_name"; return; }
        fi

        local _main_c
        _main_c=$(grep -rl 'int main\s*(' "$src"/*.c "$src"/*.cpp 2>/dev/null \
            | grep -viE 'test|helper|util|example|sample|bench|compat' \
            | head -n1 || true)
        if [[ -n "$_main_c" ]]; then
            local _bin_name
            _bin_name=$(basename "${_main_c%.*}")
            if [[ "$_bin_name" != "main" && "$_bin_name" != "src" ]]; then
                echo "$_bin_name"; return
            fi
        fi

        echo "$pkg"; return
    fi

    if [[ "$method" == "npm" ]]; then
        local _bin
        _bin=$(python3 -c "import json,sys; d=json.load(open('$src/package.json')); \
            b=d.get('bin',{}); \
            print(list(b.keys())[0] if isinstance(b,dict) and b else d.get('main',''))" \
            2>/dev/null || true)
        [[ -n "$_bin" ]] && { echo "$_bin"; return; }
        echo "$pkg"; return
    fi

    if [[ "$method" == "ruby" ]]; then
        f=$(ls "$src"/*.rb 2>/dev/null \
            | grep -viE 'spec|test|helper|config|gemspec' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
        echo "$pkg"; return
    fi

    if [[ "$method" == "lua" ]]; then
        [[ -f "$src/$pkg.lua" ]] && { echo "$pkg.lua"; return; }
        f=$(ls "$src"/*.lua 2>/dev/null | grep -viE 'test|spec|config' | head -n1 || true)
        [[ -n "$f" ]] && { basename "$f"; return; }
    fi

    f=$(find "$src" -maxdepth 1 -type f ! -name "*.*" 2>/dev/null \
        | while IFS= read -r _ef; do
            grep -qU $'\x00' "$_ef" 2>/dev/null && continue
            _sh=$(head -n1 "$_ef" 2>/dev/null || true)
            echo "$_sh" | grep -qE '^#!.*(bash|sh|python|perl|ruby)\b' && echo "$_ef"
          done \
        | grep -viE 'Makefile|configure|install|setup|uninstall|update|test' \
        | head -n1 || true)
    [[ -n "$f" ]] && { basename "$f"; return; }

    echo "$pkg"
}

make_install_block() {
    local method="$1"
    local pkg="$2"
    local main="$3"
    local deps_joined="$4"
    local pip_extra="${5:-}"
    local installer="${6:-}"
    local cpan_mods="${7:-}"
    local python_ver="${8:-3}"

    local pip_extra_cmd=""
    local _pip_cmd="pip"
    [[ "$python_ver" == "2" ]] && _pip_cmd="pip2"
    if [[ -n "$pip_extra" ]]; then
        local _dep_lines=""
        for _dep in $pip_extra; do
            _dep_lines+="    ${_pip_cmd} install --quiet ${_dep} --break-system-packages 2>/dev/null || echo \"[ WARN ] pip install ${_dep} failed — may be missing at runtime\"\n"
        done
        pip_extra_cmd=$(printf '%b' "$_dep_lines")
    fi

    local installer_cmd=""
    if [[ -n "$installer" ]]; then
        installer_cmd='
    if [[ -f "$libdir/'"$installer"'" ]]; then
        echo "[ INFO ] Running '"$installer"'..."
        (cd "$libdir" && bash '"$installer"' 2>/dev/null || true)
        echo "[ INFO ] Installer selesai"
    fi'
    fi

    case "$method" in

    pip)
cat <<BLOCK
TERMUX_PKG_DEPENDS="${deps_joined}"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
${pip_extra_cmd}
    local libdir="\$TERMUX_PREFIX/lib/${pkg}"
    pip install . --prefix="\$TERMUX_PREFIX" --break-system-packages 2>/dev/null \\
        || pip install . --prefix="\$TERMUX_PREFIX" --no-build-isolation --break-system-packages 2>/dev/null \\
        || pip install . --prefix="\$TERMUX_PREFIX" --no-deps --no-build-isolation --break-system-packages || {
            echo "pip failed — falling back to manual install"
            mkdir -p "\$libdir"
            cp -r . "\$libdir/"
        }

    find "\$libdir" -type d 2>/dev/null | while read -r _dir; do
        if ls "\$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "\$_dir/__init__.py" ]]; then
            touch "\$_dir/__init__.py"
        fi
    done

${installer_cmd}
}
BLOCK
    ;;

    python-script)
cat <<BLOCK
TERMUX_PKG_DEPENDS="${deps_joined}$(  [[ "$python_ver" == "2" ]] && echo ", python2" || true )"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    ${_pip_cmd} install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
${pip_extra_cmd}

    local libdir="\$TERMUX_PREFIX/lib/${pkg}"
    mkdir -p "\$libdir"
    cp -r . "\$libdir/"

    find "\$libdir" -type d | while read -r _dir; do
        if ls "\$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "\$_dir/__init__.py" ]]; then
            touch "\$_dir/__init__.py"
        fi
    done

${installer_cmd}

    cat > "\$TERMUX_PREFIX/bin/${pkg}" <<'WRAPPER'
#!/usr/bin/env bash
cd "\${TERMUX_PREFIX}/lib/${pkg}" || exit 1
exec python${python_ver} "\${TERMUX_PREFIX}/lib/${pkg}/${main}" "\$@"
WRAPPER
    sed -i "s|\\\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "\$TERMUX_PREFIX/bin/${pkg}"
    chmod 0755 "\$TERMUX_PREFIX/bin/${pkg}"
}
BLOCK
    ;;

    shell)
cat <<BLOCK
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="\$TERMUX_PREFIX/lib/${pkg}"

    local _has_support=false
    for _dir in core lib modules plugins data assets resources config; do
        [[ -d "\$_dir" ]] && _has_support=true && break
    done

    if [[ "\$_has_support" == true ]]; then
        mkdir -p "\$libdir"
        cp -r . "\$libdir/"
        chmod 0755 "\$libdir/${main}"

        mkdir -p "\$TERMUX_PREFIX/bin"
        printf '#!/data/data/com.termux/files/usr/bin/bash\nexec bash "%s" "\$@"\n' \
            "\$libdir/${main}" > "\$TERMUX_PREFIX/bin/${pkg}"
        chmod 0755 "\$TERMUX_PREFIX/bin/${pkg}"
    else
        install -Dm755 "${main}" "\$TERMUX_PREFIX/bin/${pkg}"
    fi
}
BLOCK
    ;;

    cmake)
cat <<BLOCK
TERMUX_PKG_DEPENDS="libandroid-support"
TERMUX_PKG_EXTRA_CONFIGURE_ARGS="
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX=\$TERMUX_PREFIX
"
BLOCK
    ;;

    autotools)
cat <<BLOCK

termux_step_pre_configure() {
    [[ -f configure.ac ]] && autoreconf -fi
}

termux_step_make_install() {
    make install PREFIX="\$TERMUX_PREFIX" DESTDIR="" \
        || make install prefix="\$TERMUX_PREFIX" DESTDIR=""
}
BLOCK
    ;;


    make)
cat <<BLOCK

termux_step_make() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found in \$(pwd) — skipping make step"
        return 0
    fi

    local _mk_target=""
    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    if grep -qE "^${pkg}[[:space:]]*:" "\$_mk_file" 2>/dev/null; then
        _mk_target="${pkg}"
    elif grep -qE "^(unix|linux|android)[[:space:]]*:" "\$_mk_file" 2>/dev/null; then
        _mk_target=\$(grep -E "^(unix|linux|android)[[:space:]]*:" "\$_mk_file" \
            | head -n1 | sed 's/[[:space:]]*:.*//')
    fi

    if [[ -n "\$_mk_target" ]]; then
        make -j"\$(nproc)" PREFIX="\$TERMUX_PREFIX" "\$_mk_target" 2>/dev/null \
            || make PREFIX="\$TERMUX_PREFIX" "\$_mk_target"
    else
        make -j"\$(nproc)" PREFIX="\$TERMUX_PREFIX" 2>/dev/null \
            || make PREFIX="\$TERMUX_PREFIX"
    fi
}

termux_step_make_install() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found — skipping install step"
        return 1
    fi

    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    local _install_ok=false
    if grep -qE "^install[[:space:]]*:" "\$_mk_file" 2>/dev/null; then
        if grep -A5 "^install:" "\$_mk_file" 2>/dev/null \
                | grep -qE '\$\(PREFIX\)|\$\(DESTDIR\)|\$\(prefix\)'; then
            make install PREFIX="\$TERMUX_PREFIX" DESTDIR="" 2>/dev/null \
                && _install_ok=true
        fi
    fi

    if [[ "\$_install_ok" == true ]]; then
        return 0
    fi

    echo "[ INFO ] make install tidak support PREFIX — mencari binary hasil build..."
    local _bin=""

    local _mk_binary
    _mk_binary=\$(grep -oE '\-o[[:space:]]+[a-zA-Z0-9_-]+' "\$_mk_file" 2>/dev/null \
        | grep -viE '\-o[[:space:]]+(\.o|\.exe|.*\.o)' \
        | head -n1 | awk '{print \$2}' || true)

    for _candidate in "\$_mk_binary" "${pkg}" "${pkg}.out" "${pkg}-bin"; do
        [[ -z "\$_candidate" ]] && continue
        if [[ -f "\$_candidate" && -x "\$_candidate" ]]; then
            _bin="\$_candidate"; break
        fi
    done

    if [[ -z "\$_bin" ]]; then
        _bin=\$(find . -maxdepth 1 -type f -perm /111 \
            ! -name "*.sh" ! -name "*.py" ! -name "*.pl" \
            ! -name "Makefile" ! -name "makefile" ! -name "configure" \
            ! -name "*.c" ! -name "*.h" ! -name "*.o" \
            2>/dev/null | head -n1 || true)
    fi

    if [[ -n "\$_bin" ]]; then
        echo "[ INFO ] Binary ditemukan: \$_bin"
        install -Dm755 "\$_bin" "\$TERMUX_PREFIX/bin/${pkg}"
        echo "[ OK ] Installed: \$TERMUX_PREFIX/bin/${pkg}"
    else
        echo "[ WARN ] Binary tidak ditemukan — install manual diperlukan"
        echo "[ WARN ] Edit termux_step_make_install() di build.sh"
        return 1
    fi
}
BLOCK
    ;;

    cargo)
cat <<BLOCK
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "\$TERMUX_PREFIX"
}
BLOCK
    ;;

    go)
cat <<BLOCK
TERMUX_PKG_DEPENDS="golang"

termux_step_make_install() {
    export GOPATH="\$PWD/gopath"
    export GOPROXY="https://proxy.golang.org,direct"
    if [[ -f go.mod ]]; then
        go get ./... 2>/dev/null || true
        go build -v -o "\$TERMUX_PREFIX/bin/${pkg}" .
    else
        go mod init "${pkg}" 2>/dev/null || true
        go get ./... 2>/dev/null || true
        go mod tidy 2>/dev/null || true
        go build -v -o "\$TERMUX_PREFIX/bin/${pkg}" . 2>/dev/null \
            || go build -v -o "\$TERMUX_PREFIX/bin/${pkg}" *.go
    fi
}
BLOCK
    ;;

    npm)
cat <<BLOCK
TERMUX_PKG_DEPENDS="nodejs"

termux_step_make_install() {
    npm install --prefix "\$TERMUX_PREFIX" -g .
}
BLOCK
    ;;

    ruby)
cat <<BLOCK
TERMUX_PKG_DEPENDS="ruby"

termux_step_make_install() {
    [[ -f *.gemspec ]] \\
        && gem build *.gemspec && gem install --local *.gem --no-document \\
        || { mkdir -p "\$TERMUX_PREFIX/lib/${pkg}"; cp -r . "\$TERMUX_PREFIX/lib/${pkg}/"; }
}
BLOCK
    ;;

    perl)
cat <<BLOCK
TERMUX_PKG_DEPENDS="${deps_joined}"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="\$TERMUX_PREFIX/lib/${pkg}"
    mkdir -p "\$libdir"

    cp -r . "\$libdir/"

    if command -v cpanm >/dev/null 2>&1 || command -v cpan >/dev/null 2>&1; then
        echo "  Installing CPAN dependencies..."
        local _cpanm
        command -v cpanm &>/dev/null && _cpanm="cpanm --quiet" || _cpanm="cpan -T"
        local _mods="${cpan_mods}"
        for _mod in \$_mods; do
            perl -e "require \$_mod; 1" 2>/dev/null && continue
            echo "    + \$_mod"
            \$_cpanm "\$_mod" 2>/dev/null || true
        done
    else
        echo "  TIP: Install cpanm for automatic CPAN dep install: pkg install perl-app-cpanminus"
    fi

    if [[ -f "\$libdir/Makefile.PL" ]]; then
        cd "\$libdir"
        perl Makefile.PL PREFIX="\$TERMUX_PREFIX" 2>/dev/null && make && make install || true
    elif [[ -f "\$libdir/Build.PL" ]]; then
        cd "\$libdir"
        perl Build.PL --install_base="\$TERMUX_PREFIX" 2>/dev/null && \
            perl Build && perl Build install || true
    fi

    if [[ -f "\$libdir/${main}" ]]; then
        chmod 0755 "\$libdir/${main}"
        mkdir -p "\$TERMUX_PREFIX/bin"
        cat > "\$TERMUX_PREFIX/bin/${pkg}" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
cd "/data/data/com.termux/files/usr/lib/${pkg}" || exit 1
exec perl "/data/data/com.termux/files/usr/lib/${pkg}/${main}" "\$@"
WRAPPER
        chmod 0755 "\$TERMUX_PREFIX/bin/${pkg}"
    fi
}
BLOCK
    ;;

    lua)
cat <<BLOCK
TERMUX_PKG_DEPENDS="lua54"

termux_step_make_install() {
    install -Dm755 "${main}" "\$TERMUX_PREFIX/bin/${pkg}"
}
BLOCK
    ;;

    php)
cat <<BLOCK
TERMUX_PKG_DEPENDS="php"

termux_step_make_install() {
    mkdir -p "\$TERMUX_PREFIX/lib/${pkg}"
    cp -r . "\$TERMUX_PREFIX/lib/${pkg}/"
    cat > "\$TERMUX_PREFIX/bin/${pkg}" <<'WRAPPER'
#!/usr/bin/env bash
exec php "/data/data/com.termux/files/usr/lib/${pkg}/${main}" "$@"
WRAPPER
    chmod 0755 "\$TERMUX_PREFIX/bin/${pkg}"
}
BLOCK
    ;;

    *)
cat <<BLOCK

termux_step_make_install() {
    echo "⚠️ Unknown build system — edit this function manually"
    mkdir -p "\$TERMUX_PREFIX/lib/${pkg}"
    cp -r . "\$TERMUX_PREFIX/lib/${pkg}/"
}
BLOCK
    ;;
    esac
}

github_api() {
    local url="$1"
    local result
    result=$(curl -sf \
        -H "Accept: application/vnd.github+json" \
        ${GITHUB_TOKEN:+-H "Authorization: Bearer $GITHUB_TOKEN"} \
        "$url" 2>/dev/null) || true

    case "$result" in
        *rate\ limit*|*API\ rate\ limit*)
            warn "GitHub API rate limited — set GITHUB_TOKEN env var for higher limits"
            echo "" ;;
        *)
            echo "$result" ;;
    esac
}

json_field() {
    local json="$1" field="$2"
    echo "$json" | sed -n "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -n1
}


gitlab_api() {
    local url="$1"
    local result
    result=$(curl -sf \
        -H "Accept: application/json" \
        ${GITLAB_TOKEN:+-H "PRIVATE-TOKEN: $GITLAB_TOKEN"} \
        "$url" 2>/dev/null) || true

    case "$result" in
        *rate\ limit*|*error*Retry*)
            warn "GitLab API rate limited — set GITLAB_TOKEN env var for higher limits"
            echo "" ;;
        *)
            echo "$result" ;;
    esac
}

forge_fetch_metadata() {
    local repo_url="$1"

    if [[ "$repo_url" == *"github.com"* ]]; then
        step "Fetching GitHub metadata"

        local api_base
        api_base=$(echo "$repo_url" \
            | sed 's#https://github.com/#https://api.github.com/repos/#' \
            | sed 's#\.git$##')

        local data
        data=$(github_api "$api_base")

        if [[ -n "$data" ]]; then
            DESCRIPTION=$(json_field "$data" "description")
            [[ -z "$DESCRIPTION" || "$DESCRIPTION" == "null" ]] && \
                DESCRIPTION="$PKG_NAME — auto-packaged by termux-build-init"
            LICENSE=$(json_field "$data" "spdx_id");   LICENSE="${LICENSE:-UNKNOWN}"
            LANGUAGE=$(json_field "$data" "language");  LANGUAGE="${LANGUAGE:-Unknown}"
            HOMEPAGE=$(json_field "$data" "homepage");  HOMEPAGE="${HOMEPAGE:-$repo_url}"
            [[ -z "$HOMEPAGE" || "$HOMEPAGE" == "null" ]] && HOMEPAGE="$repo_url"
            ok "Repo: ${W}${DESCRIPTION}${N}"
        fi

        local release tag
        release=$(github_api "$api_base/releases/latest")
        tag=$(json_field "$release" "tag_name") || true

        if [[ -n "$tag" ]]; then
            VERSION="${tag#v}"
            SRCURL="$repo_url/archive/refs/tags/$tag.tar.gz"
            ok "Source: release ${W}${tag}${N}"
        else
            local default_branch
            default_branch=$(json_field "$data" "default_branch")

            if [[ -z "$default_branch" || "$default_branch" == "null" ]]; then
                warn "Could not detect default branch — probing common names..."
                for _b in master main trunk dev; do
                    if curl -sf --head "$repo_url/archive/refs/heads/$_b.tar.gz" \
                            -o /dev/null 2>/dev/null; then
                        default_branch="$_b"; break
                    fi
                done
                [[ -z "$default_branch" ]] && default_branch="main"
            fi

            VERSION="1.0.0"
            SRCURL="$repo_url/archive/refs/heads/$default_branch.tar.gz"
            warn "No release found — using branch ${W}${default_branch}${N}"
        fi

    elif [[ "$repo_url" == *"gitlab.com"* || "$repo_url" == *"gitlab."* ]]; then
        step "Fetching GitLab metadata"

        local gl_host gl_path gl_path_encoded api_base
        gl_host=$(echo "$repo_url" | sed 's#https://\([^/]*\)/.*#\1#')
        gl_path=$(echo "$repo_url" | sed "s#https://${gl_host}/##" | sed 's#\.git$##')
        gl_path_encoded=$(echo "$gl_path" | sed 's#/#%2F#g')
        api_base="https://${gl_host}/api/v4/projects/${gl_path_encoded}"

        local data
        data=$(gitlab_api "$api_base")

        if [[ -n "$data" ]]; then
            DESCRIPTION=$(json_field "$data" "description")
            [[ -z "$DESCRIPTION" || "$DESCRIPTION" == "null" ]] && \
                DESCRIPTION="$PKG_NAME — auto-packaged by termux-build-init"
            local lic
            lic=$(echo "$data" | sed -n 's/.*"license"[^}]*"key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
            LICENSE="${lic:-UNKNOWN}"
            LANGUAGE="Unknown"
            local web_url
            web_url=$(json_field "$data" "web_url")
            HOMEPAGE="${web_url:-$repo_url}"
            ok "Repo: ${W}${DESCRIPTION}${N}"
        fi

        local releases tag
        releases=$(gitlab_api "$api_base/releases?per_page=1")
        tag=$(json_field "$releases" "tag_name") || true

        if [[ -n "$tag" ]]; then
            VERSION="${tag#v}"
            SRCURL="$repo_url/-/archive/$tag/${PKG_NAME}-${tag}.tar.gz"
            ok "Source: release ${W}${tag}${N}"
        else
            local default_branch
            default_branch=$(json_field "$data" "default_branch")
            [[ -z "$default_branch" || "$default_branch" == "null" ]] && \
                default_branch="main"

            local probe_ok=false
            for _b in "$default_branch" master main trunk dev; do
                _probe="$repo_url/-/archive/${_b}/${PKG_NAME}-${_b}.tar.gz"
                if curl -sf --head "$_probe" -o /dev/null 2>/dev/null; then
                    default_branch="$_b"; probe_ok=true; break
                fi
            done

            VERSION="1.0.0"
            SRCURL="$repo_url/-/archive/${default_branch}/${PKG_NAME}-${default_branch}.tar.gz"
            warn "No release found — using branch ${W}${default_branch}${N}"
        fi

    elif [[ "$repo_url" == *"codeberg.org"* ]]; then
        step "Fetching Codeberg metadata"

        local cb_path api_base
        cb_path=$(echo "$repo_url" | sed 's#https://codeberg.org/##' | sed 's#\.git$##')
        api_base="https://codeberg.org/api/v1/repos/${cb_path}"

        local data
        data=$(curl -sf "$api_base" 2>/dev/null) || true

        if [[ -n "$data" ]]; then
            DESCRIPTION=$(json_field "$data" "description")
            [[ -z "$DESCRIPTION" || "$DESCRIPTION" == "null" ]] && \
                DESCRIPTION="$PKG_NAME — auto-packaged by termux-build-init"
            LICENSE="UNKNOWN"
            LANGUAGE="Unknown"
            HOMEPAGE="$repo_url"
            ok "Repo: ${W}${DESCRIPTION}${N}"
        fi

        local releases tag
        releases=$(curl -sf "$api_base/releases?limit=1" 2>/dev/null) || true
        tag=$(json_field "$releases" "tag_name") || true

        if [[ -n "$tag" ]]; then
            VERSION="${tag#v}"
            SRCURL="$repo_url/archive/$tag.tar.gz"
            ok "Source: release ${W}${tag}${N}"
        else
            local default_branch
            default_branch=$(json_field "$data" "default_branch")
            [[ -z "$default_branch" || "$default_branch" == "null" ]] && \
                default_branch="main"
            VERSION="1.0.0"
            SRCURL="$repo_url/archive/branch/$default_branch.tar.gz"
            warn "No release found — using branch ${W}${default_branch}${N}"
        fi

    else
        warn "Unknown forge — treating as direct download URL"
        SRCURL="$repo_url"
        VERSION="1.0.0"
        HOMEPAGE="$repo_url"
    fi
}

banner

REPO_URL="${1:-}"

step "Input"

if [[ -z "$REPO_URL" ]]; then
    read -rp "  Repo URL (GitHub/GitLab/Codeberg or direct URL): " REPO_URL
fi

PKG_NAME=$(sanitize_pkgname "$(basename "$REPO_URL")")
info "Package name: ${W}${PKG_NAME}${N}"

PKG_DIR="$PACKAGES_DIR/$PKG_NAME"
mkdir -p "$PKG_DIR"

HOMEPAGE="${REPO_URL:-https://example.com}"
DESCRIPTION="$PKG_NAME — auto-packaged by termux-build-init"
LICENSE="UNKNOWN"
VERSION="1.0.0"
SRCURL=""
SHA256="SKIP"
LANGUAGE="Unknown"
INSTALL_METHOD="unknown"
DEPENDS_RAW=""
MAIN_FILE=""

forge_fetch_metadata "$REPO_URL"

[[ -z "$SRCURL" ]] && fail "Tidak bisa menentukan source URL dari: $REPO_URL\n  Pastikan URL valid (GitHub/GitLab/Codeberg) atau masukkan URL tar.gz langsung."

step "Downloading & analyzing source"
info "URL: $SRCURL"

if ! curl -sf --head "$SRCURL" -o /dev/null 2>/dev/null; then
    printf "${BGREEN}[${BRED}FAIL${BGREEN}]${R}  Source URL is not accessible: %s\n" "$SRCURL"
    info "Check the branch name or make sure the repository is not private."
    exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

TMPTAR="$TMP/src.tar.gz"
if ! curl -fL "$SRCURL" -o "$TMPTAR" --progress-bar; then
    fail "Failed to download source"
fi
ok "Download complete"

tar -xf "$TMPTAR" -C "$TMP"
SRC=$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n1)
[[ -z "$SRC" ]] && fail "Could not extract source directory"
info "Source root: ${W}$(basename "$SRC")${N}"

echo ""
echo "  📂 Files in source:"
ls "$SRC" | sed 's/^/     /'
echo ""

step "Auto-detection"

INSTALL_METHOD=$(detect_method "$SRC")
ok "Build method : ${W}${INSTALL_METHOD}${N}"

MAIN_FILE=$(detect_entrypoint "$SRC" "$PKG_NAME" "$INSTALL_METHOD")
ok "Entrypoint   : ${W}${MAIN_FILE}${N}"

INSTALLER_SCRIPT=$(detect_installer "$SRC")
if [[ -n "$INSTALLER_SCRIPT" ]]; then
    ok "Installer    : ${W}${INSTALLER_SCRIPT}${N} ${C}(will run post-copy)${N}"
else
    info "Installer    : none detected"
fi

_BUILD_SCRIPTS_ONLY=false
if [[ "$INSTALL_METHOD" == "unknown" ]]; then
    _ROOT_FILES=$(ls "$SRC" 2>/dev/null | grep -vE '^(LICENSE|README|\.git|\.github|Makefile|CMakeLists)' | head -20)
    _HAS_SCRIPTS_DIR=false
    _HAS_PATCHES_DIR=false
    _HAS_NO_BINARY=true
    [[ -d "$SRC/scripts" ]]  && _HAS_SCRIPTS_DIR=true
    [[ -d "$SRC/patches" ]]  && _HAS_PATCHES_DIR=true
    [[ -d "$SRC/cmake" ]]    && _HAS_PATCHES_DIR=true
    _RUNNABLE=$(find "$SRC" -maxdepth 1 -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.rb" \) 2>/dev/null | head -1)
    [[ -n "$_RUNNABLE" ]] && _HAS_NO_BINARY=false

    if [[ "$_HAS_SCRIPTS_DIR" == true || "$_HAS_PATCHES_DIR" == true ]] && [[ "$_HAS_NO_BINARY" == true ]]; then
        _BUILD_SCRIPTS_ONLY=true
    fi
fi

PYTHON_VERSION="3"
if [[ "$INSTALL_METHOD" == "python-script" || "$INSTALL_METHOD" == "pip" ]]; then
    PYTHON_VERSION=$(detect_python_version "$SRC" "$MAIN_FILE")
    if [[ "$PYTHON_VERSION" == "2" ]]; then
        echo ""
        echo -e "  ${R}┌─ Python 2 Not Supported ────────────────────────────────────┐${N}"
        echo -e "  ${R}│${N}                                                             ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}This package requires Python 2, which is not accepted${N}      ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}in Termux App Store.${N}                                       ${R}│${N}"
        echo -e "  ${R}│${N}                                                             ${R}│${N}"
        echo -e "  ${R}│${N}  ${Y}Python 2 is End-of-Life and no longer supported.${N}           ${R}│${N}"
        echo -e "  ${R}│${N}  ${Y}pip2 cannot install modern dependencies.${N}                   ${R}│${N}"
        echo -e "  ${R}│${N}                                                             ${R}│${N}"
        echo -e "  ${R}│${N}  ${C}Need help? Open an issue on GitHub:${N}                        ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}https://github.com/djunekz/termux-app-store/issues${N}         ${R}│${N}"
        echo -e "  ${R}│${N}                                                             ${R}│${N}"
        echo -e "  ${R}└─────────────────────────────────────────────────────────────┘${N}"
        echo ""
        exit 1
    fi
fi

step "Dependency scan"

DEPS_DECLARED=""
DEPS_IMPORTS=""
DEPS_PERL_PKG=""
DEPS_PERL_CPAN=""

DEPS_SHELL_WARNS=""
DEPS_SHELL_PKGS=""

if [[ "$INSTALL_METHOD" == "pip" || "$INSTALL_METHOD" == "python-script" ]]; then
    DEPS_DECLARED=$(scan_python_declared_deps "$SRC" || true)
    DEPS_IMPORTS=$(scan_python_imports "$SRC" || true)
    info "Declared deps : ${DEPS_DECLARED:-none}"
    info "Import deps   : ${DEPS_IMPORTS:-none}"
fi

if [[ "$INSTALL_METHOD" == "perl" ]]; then
    _PERL_CPAN_TMP=$(mktemp)
    DEPS_PERL_PKG=$(scan_perl_deps "$SRC" 2>"$_PERL_CPAN_TMP" || true)
    DEPS_PERL_CPAN=$(sed 's/^cpan: //' "$_PERL_CPAN_TMP" 2>/dev/null || true)
    rm -f "$_PERL_CPAN_TMP"
    info "Perl pkg deps : ${DEPS_PERL_PKG:-none}"
    [[ -n "$DEPS_PERL_CPAN" ]] && info "CPAN modules  : ${DEPS_PERL_CPAN}"
fi

DEPS_SHELL_RAW=$(scan_shell_deps "$SRC" || true)
if [[ -n "$DEPS_SHELL_RAW" ]]; then
    DEPS_SHELL_WARNS=$(printf '%s
' $DEPS_SHELL_RAW | grep '^warn:' | sed 's/^warn://' | xargs || true)
    DEPS_SHELL_PKGS=$(printf '%s
' $DEPS_SHELL_RAW | grep '^pkg:' | xargs || true)
    [[ -n "$DEPS_SHELL_WARNS" ]] && warn "Incompatible  : ${R}${DEPS_SHELL_WARNS}${N}"
    [[ -n "$DEPS_SHELL_PKGS"  ]] && info "Shell deps    : ${DEPS_SHELL_PKGS}"
fi

case "$INSTALL_METHOD" in
    pip|python-script)
        ALL_DEPS="$DEPS_DECLARED $DEPS_IMPORTS ${DEPS_SHELL_PKGS:-}"
        PKG_ONLY_DEPS=$(pkg_deps "pkg:python pkg:python-pip pkg:python-setuptools $ALL_DEPS")
        PIP_ONLY_DEPS=$(pip_deps "$ALL_DEPS") ;;
    cargo)      ALL_DEPS="rust" ;;
    go)         ALL_DEPS="golang" ;;
    npm)        ALL_DEPS="nodejs" ;;
    cmake)      ALL_DEPS="libandroid-support" ;;
    ruby)       ALL_DEPS="ruby" ;;
    perl)
        _PERL_PKG_LIST="perl ${DEPS_PERL_PKG:-}"
        ALL_DEPS=$(echo "$_PERL_PKG_LIST" | tr ' ' '\n' | sed 's|^pkg:||g' | sort -u | grep -v '^$' | xargs)
        ;;
    lua)        ALL_DEPS="lua54" ;;
    php)        ALL_DEPS="php" ;;
    shell|make|autotools|unknown) ALL_DEPS="${DEPS_SHELL_PKGS:-}" ;;
    *)          ALL_DEPS="" ;;
esac

if [[ "$INSTALL_METHOD" != "pip" && "$INSTALL_METHOD" != "python-script" ]]; then
    PKG_ONLY_DEPS="${ALL_DEPS:-}"
    PIP_ONLY_DEPS=""
fi

if [[ -n "${PKG_ONLY_DEPS:-}" ]]; then
    DEPENDS_JOINED=$(join_deps "$PKG_ONLY_DEPS")
else
    DEPENDS_JOINED=""
fi
ok "pkg deps : ${W}${DEPENDS_JOINED:-none}${N}"
ok "pip deps : ${W}${PIP_ONLY_DEPS:-none}${N}"

step "Checksum"

read -rp "  Compute SHA256 automatically? [Y/n]: " _SHA
_SHA="${_SHA:-Y}"
if [[ ! "$_SHA" =~ ^[Nn]$ ]]; then
    SHA256=$(sha256sum "$TMPTAR" | awk '{print $1}')
    ok "SHA256: ${W}${SHA256}${N}"
else
    SHA256="SKIP"
    warn "SHA256 set to SKIP — verification disabled"
fi

echo ""
_sl=$(printf '%.0s─' $(seq 1 44))
echo -e "${W}════════════════════════════════════════════${N}"
echo -e "${W}  Smart Detection Result                    ${N}"
echo -e "${W}════════════════════════════════════════════${N}"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Package"    "$PKG_NAME"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Language"   "$LANGUAGE"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Method"     "$INSTALL_METHOD"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Version"    "$VERSION"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "License"    "$LICENSE"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Entrypoint" "$MAIN_FILE"
printf "${W}${N}  %-12s : %-28s ${W}${N}\n" "Installer"  "${INSTALLER_SCRIPT:-none}"
printf "${BCYAN}${_sl}${R}\n"
printf "  ${GRAY}%-14s${R} ${DIM}%s${R}\n" "Depends      :" "${DEPENDS_JOINED:-none}"
[[ -n "${DEPS_SHELL_WARNS:-}" ]] && printf " ${GRAY}%-14s${R} ${BRED}%s${R}\n" "Incompatible:" "${DEPS_SHELL_WARNS}"
printf "${BCYAN}${_sl}${R}\n"
echo ""

if [[ -n "${DEPS_SHELL_WARNS:-}" ]]; then
    _CRITICAL_WARNS=$(echo "$DEPS_SHELL_WARNS" | tr ' ' '\n' | grep -E 'iptables|hostapd|dhcpd|systemctl|airmon|ifconfig|iwconfig|rfkill|modprobe' || true)
    if [[ -n "$_CRITICAL_WARNS" ]]; then
        echo -e "  ${R}┌─ Termux-Incompatible Tool Detected ──────────────────────┐${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}This package requires system-level tools that are not${N}   ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}available on Termux/Android:${N}                            ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        while IFS= read -r _w; do
            [[ -z "$_w" ]] && continue
            _tool=$(echo "$_w" | sed 's/-.*//')
            printf "  ${R}│${N}   ${Y}✗  %-52s${R}│${N}\n" "$_tool"
        done <<< "$(echo "$_CRITICAL_WARNS" | tr ' ' '\n')"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${C}This tool is designed for Linux desktop, not Android.${N}   ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${C}Need help? Open an issue on GitHub:${N}                     ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}https://github.com/djunekz/termux-app-store/issues${N}      ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}└──────────────────────────────────────────────────────────┘${N}"
        echo ""
        exit 1
    fi
fi

if [[ "$INSTALL_METHOD" == "unknown" ]]; then
    echo ""
    if [[ "$_BUILD_SCRIPTS_ONLY" == true ]]; then
        echo -e "  ${R}┌─ Repo Is Not a Standalone Tool ──────────────────────────┐${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}This repository appears to be a build-scripts or${N}       ${R}│${N}"
        echo -e "  ${R}│${N}  ${W}patch collection, not a runnable application.${N}          ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${Y}Found:  scripts/  patches/  or cmake/ without any${N}      ${R}│${N}"
        echo -e "  ${R}│${N}  ${Y}runnable entrypoint (.py .sh .js .rb) in root.${N}         ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}│${N}  ${C}Packaging this repo will produce a .deb that installs${N}  ${R}│${N}"
        echo -e "  ${R}│${N}  ${C}files but no usable command.${N}                           ${R}│${N}"
        echo -e "  ${R}│${N}                                                          ${R}│${N}"
        echo -e "  ${R}└──────────────────────────────────────────────────────────┘${N}"
        echo ""
        read -rp "  Lanjutkan anyway dan edit build.sh manual? [y/N]: " _CONT_UNK
        [[ ! "${_CONT_UNK:-N}" =~ ^[Yy]$ ]] && { echo -e "  ${C}Aborted.${N}"; echo ""; exit 0; }
    else
        echo -e "  ${Y}┌─ Unknown Build System ───────────────────────────────────┐${N}"
        echo -e "  ${Y}│${N}                                                          ${Y}│${N}"
        echo -e "  ${Y}│${N}  ${W}Could not auto-detect how to build this package.${N}       ${Y}│${N}"
        echo -e "  ${Y}│${N}                                                          ${Y}│${N}"
        echo -e "  ${Y}│${N}  ${C}A placeholder build.sh will be created.${N}                ${Y}│${N}"
        echo -e "  ${Y}│${N}  ${C}You must edit termux_step_make_install() manually${N}       ${Y}│${N}"
        echo -e "  ${Y}│${N}  ${C}before running a test build.${N}                           ${Y}│${N}"
        echo -e "  ${Y}│${N}                                                          ${Y}│${N}"
        echo -e "  ${Y}└──────────────────────────────────────────────────────────┘${N}"
        echo ""
        read -rp "  Continue and edit build.sh manually? [y/N]: " _CONT_UNK
        [[ ! "${_CONT_UNK:-N}" =~ ^[Yy]$ ]] && { echo -e "  ${C}Aborted.${N}"; echo ""; exit 0; }
    fi
    echo ""
fi

read -rp "  Continue? [Y/n]: " _CONT
[[ "${_CONT:-Y}" =~ ^[Nn]$ ]] && exit 0

step "Writing build.sh"

INSTALL_BLOCK=$(make_install_block "$INSTALL_METHOD" "$PKG_NAME" "$MAIN_FILE" "$DEPENDS_JOINED" "${PIP_ONLY_DEPS:-}" "${INSTALLER_SCRIPT:-}" "${DEPS_PERL_CPAN:-}" "${PYTHON_VERSION:-3}")

{
    printf 'TERMUX_PKG_HOMEPAGE=%s\n'          "$HOMEPAGE"
    printf 'TERMUX_PKG_DESCRIPTION="%s"\n'     "$DESCRIPTION"
    printf 'TERMUX_PKG_LICENSE="%s"\n'         "$LICENSE"
    printf 'TERMUX_PKG_MAINTAINER="@termux-app-store"\n'
    printf 'TERMUX_PKG_VERSION=%s\n'           "$VERSION"
    printf 'TERMUX_PKG_SRCURL=%s\n'            "$SRCURL"
    printf 'TERMUX_PKG_SHA256=%s\n'            "$SHA256"
    printf '\n'
    printf '%s\n'                              "$INSTALL_BLOCK"
} > "$PKG_DIR/build.sh"

chmod +x "$PKG_DIR/build.sh"
ok "Saved: ${W}${PKG_DIR}/build.sh${N}"

echo ""
echo -e "${Y}--- build.sh preview ---${G}"
cat "$PKG_DIR/build.sh"
echo -e "${Y}------------------------${N}"

if [[ -f "$BUILD_SCRIPT" ]]; then
    if [[ "$INSTALL_METHOD" == "unknown" ]]; then
        echo ""
        echo -e "  ${Y}  Test build skipped — edit build.sh first, then run:${N}"
        echo -e "  ${C}  bash build-package.sh ${PKG_NAME}${N}"
        echo ""
    else
        echo ""
        read -rp "  Run test build now? [y/N]: " _TEST
        if [[ "${_TEST:-N}" =~ ^[Yy]$ ]]; then
            step "Test Build"
            bash "$BUILD_SCRIPT" "$PKG_NAME" || warn "Build finished with errors (see above)"
        fi
    fi
else
    warn "build-package.sh not found — skipping test build"
fi

echo ""
echo -e "${G}══════════════════════════════${N}"
echo -e "${G} ✅  Package ready!           ${N}"
echo -e "${G} 📦  packages/${PKG_NAME}     ${N}"
echo -e "${G}══════════════════════════════${N}"
echo ""
