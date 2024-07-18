import os

__APKTOOL_FILENAME__ = 'apktool.jar'
apktool_path = os.path.join(os.path.dirname(__file__), __APKTOOL_FILENAME__)


import subprocess
from typing import Literal


def get_apktool_jar():
    """Get full apktool jar path. If `apktool_path` is set to a valid file, that will be returned, otherwise it will return the "apktool.jar" file in this module.

    Args:
        filename (str, optional): Filename to search for. Defaults to APKTOOL_FILENAME.

    Returns:
        str: Full path.
    """
    global apktool_path
    
    path = apktool_path
    if not os.path.isfile(apktool_path):
        dir = os.path.dirname(__file__)
        path = os.path.join(dir, __APKTOOL_FILENAME__)

    if not os.path.exists(path):
        raise FileNotFoundError(path)
    
    return path

def run_command(
    *command: list[str],
    **kwargs,
) -> subprocess.CompletedProcess:
    """Run apktool command. All positional arguments are passed into apktool. All named arguments are passed into `subprocess.run()`.
    """
    args = ' '.join([
        "java",
        "-jar",
        get_apktool_jar(),
        *command,
    ])
    
    kwargs.setdefault('shell', True)
    kwargs.setdefault('check', True)

    return subprocess.run(
        args, 
        **kwargs,
    )

def version() -> str:
    """Get apktool version

    Returns:
        str: Version number.
    """
    return run_command(
        '--version',
        capture_output = True,
        text = True,
    ).stdout.strip('\n')

def decode(
    path: str,
    output: str = None,
    force: bool = False,
    *,
    decode_resources: bool = True,
    decode_sources: bool = True,
    keep_broken_resources: bool = False,
    keep_assets: bool = True,
    only_main_classes: bool = False,

    frameworks_path: str = None,
    framework_tag: str = None,
    
    api_level: int = None,
    
    force_manifest: bool = None,
    match_original: bool = None,
    resource_mode: Literal['remove', 'dummy', 'keep'] = None,

    debug_info: bool = False,
    quiet: bool = False,
    verbose: bool = False,
):
    """Decode apk. Wrapper for `apktool decode`. Arguments do not align exactly with apktool.
    
    More information here: https://apktool.org/docs/cli-parameters#decoding-options
    
    Args:
        path (str): Path to apk.
        output (str, optional): The name of folder that gets written. (default: apk.out). Defaults to `None`.
        force (bool, optional): Force delete destination directory. Defaults to `False`.
        decode_resources (bool, optional): Decode resources. Defaults to `True`.
        decode_sources (bool, optional): Decode sources. Defaults to `True`.
        keep_broken_resources (bool, optional): Use if there was an error and some resources were dropped, e.g. "Invalid config flags detected. Dropping resources", but you want to decode them anyway, even with errors. You will have to fix them manually before building.. Defaults to `False`.
        keep_assets (bool, optional): Decode assets. Defaults to `True`.
        only_main_classes (bool, optional): Only disassemble the main dex classes (classes[0-9]*.dex) in the root. Defaults to `False`.
        frameworks_path (str, optional): Use framework files located in `<dir>`. Defaults to `None`.
        framework_tag (str, optional): Use framework files tagged by `<tag>`. Defaults to `None`.
        api_level (int, optional): The numeric api-level of the file to generate, e.g. 14 for ICS. Defaults to `None`.
        force_manifest (bool, optional): Decode the APK's compiled manifest, even if `decode_resources` is set to `false`. Defaults to `None`.
        match_original (bool, optional): Keep files to closest to original as possible (prevents rebuild). Defaults to None.
        resource_mode (Literal['remove', 'dummy', 'keep'], optional): Sets the resolve resources mode. Possible values are: 'remove' (default), 'dummy' or 'keep'. Defaults to `None`.
        debug_info (bool, optional): Prevents baksmali from writing out debug info. (.local, .param, .line, etc.).. Defaults to `False`.
        quiet (bool, optional): Don't print anything. Defaults to `False`.
        verbose (bool, optional): Print verbose logging. Defaults to `False`.
    """
    
    args = []
    
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    
    args.extend(['decode', path])

    if output:
        args.extend(['--output', output])
    if force:
        args.append('--force')
    
    if debug_info:
        args.append('--no-debug-info')
    
    if not decode_resources:
        args.append('--no-res')
    if not decode_sources:
        args.append('--no-src')
    
    if keep_broken_resources:
        args.append('--keep-broken-res')
    if not keep_assets:
        args.append('--no-assets')
    if only_main_classes:
        args.append('--only-main-classes')
    
    if frameworks_path:
        args.extend(['--frame-path', frameworks_path])
    if framework_tag:
        args.extend(['--frame-tag', framework_tag])
    
    if api_level != None:
        args.extend(['--api-level', str(api_level)])
    
    if force_manifest:
        args.append('--force-manifest')
    if match_original:
        args.append('--match-original')
    if resource_mode:
        args.append('--resource-mode')
    
    return run_command(*args)

def build(
    path: str,
    output: str = None,
    *,
    api_level: int = None,
    debug: bool = False,
    copy_original: bool = False,

    force_all: bool = False,
    crunch_resources: bool = True,
    frameworks_path: str = False,

    network_security_config: bool = False,
    
    aapt_path: str = None,
    use_appt1: bool = False,
    
    quiet: bool = False,
    verbose: bool = False,
):
    """Build apk. Wrapper for `apktool build`. Arguments do not align exactly with apktool.
    
    More information here: https://apktool.org/docs/cli-parameters#building-options

    Args:
        path (str): Folder of decoded apk.
        output (str, optional): The name of apk that gets written. (default: dist/name.apk). Defaults to `None`.
        api_level (int, optional): The numeric api-level of the file to generate, e.g. 14 for ICS. Defaults to `None`.
        debug (bool, optional): Set android:debuggable to "true" in the APK's compiled manifest. Defaults to `False`.
        copy_original (bool, optional): Copy original AndroidManifest.xml and META-INF. See apktool webpage for more info. Defaults to `False`.
        force_all (bool, optional): Skip changes detection and build all files. Defaults to `False`.
        crunch_resources (bool, optional): Enables crunching of resource files during the build step. Defaults to `True`.
        frameworks_path (str, optional): Use framework files located in `<dir>`. Defaults to `False`.
        network_security_config (bool, optional): Add a generic Network Security Configuration file in the output APK. Defaults to `False`.
        aapt_path (str, optional): Load aapt from specified location. Defaults to `None`.
        use_appt1 (bool, optional): Use aapt binary instead of aapt2 during the build step. Defaults to `False`.
        quiet (bool, optional): Don't print anything. Defaults to `False`.
        verbose (bool, optional): Print verbose logging. Defaults to `False`.
    """
    args = []
    
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    
    args.append(['build', path])
    
    if output:
        args.extend(['--output', output])
    
    if api_level != None:
        args.extend(['--api-level', str(api_level)])
    
    if debug:
        args.append('--debug')
    if copy_original:
        args.append('--copy-original')
    if force_all:
        args.append('--force-all')
    if not crunch_resources:
        args.append('--no-crunch')
    if frameworks_path:
        args.extend(['--frame-path', frameworks_path])
    if network_security_config:
        args.append('--net-sec-conf')
    if aapt_path:
        args.extend(['--aapt', aapt_path])
    if use_appt1:
        args.append('--use-aapt1')
    
    return run_command(*args)

def install_framework(
    path: str,
    frameworks_path: str = None,
    tag: str = None,
    *,
    quiet: bool = False,
    verbose: bool = False,
):
    """Install framework. Wrapper for `apktool if`. Arguments do not align exactly with apktool.

    Args:
        path (str): Path to apk framework file.
        frameworks_path (str, optional): Store framework files here. Defaults to `None`.
        tag (str, optional): Tag frameworks. Defaults to `None`.
        quiet (bool, optional): Don't print anything. Defaults to `False`.
        verbose (bool, optional): Print verbose logging. Defaults to `False`.
    """
    args = []
    
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    
    args.extend(['install-framework', path])
    
    if frameworks_path:
        args.extend(['--frame-path', frameworks_path])
    if tag:
        args.extend(['--tag', tag])
    
    return run_command(*args)

def list_frameworks(frameworks_path: str = None) -> list[str]:
    """List frameworks. Wrapper for `apktool list-frameworks`.

    More information here: https://apktool.org/docs/cli-parameters#list-framework-directory-options

    Args:
        frameworks_path (str, optional): Store framework files here. Defaults to `None`.

    Returns:
        list[str]: List of framework apks.
    """
    args = ['list-frameworks']

    if frameworks_path:
        args.extend(['--frame-path', frameworks_path])
    
    result: str = run_command(
        *args,
        capture_output = True,
        text = True,
    ).stdout
    
    return [a[3::] for a in result.splitlines()]

def empty_framework_dir(
    force: bool = False,
    frameworks_path: str = None,
    *,
    quiet: bool = False,
    verbose: bool = False,
):
    """Empty framework directory. Wrapper for `apktool empty-framework-dir`.
    
    More information here: https://apktool.org/docs/cli-parameters#empty-framework-directory-options

    Args:
        force (bool, optional): Force delete destination directory. Defaults to `False`.
        frameworks_path (str, optional):  Store framework files here. Defaults to `None`.
        quiet (bool, optional): Don't print anything. Defaults to `False`.
        verbose (bool, optional): Print verbose logging. Defaults to `False`.
    """
    args = []
    
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    
    args.append('empty-framework-dir')

    if force:
        args.append('--force')
    if frameworks_path:
        args.extend(['--frame-path', frameworks_path])
    
    return run_command(*args)

def publicize_resources(
    path: str,
    *,
    quiet: bool = False,
    verbose: bool = False,
):
    """PUblicize resources. Wrapper for `apktool publicize-resources`.

    Args:
        path (str): File path.
        quiet (bool, optional): Don't print anything. Defaults to `False`.
        verbose (bool, optional): Print verbose logging. Defaults to `False`.
    """
    args = []
    
    if quiet:
        args.append('--quiet')
    if verbose:
        args.append('--verbose')
    
    args.extend(['publicize-resources', path])

    return run_command(*args)


