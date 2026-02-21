from setuptools import setup
import re


def derive_version() -> str:
    version = ''
    with open('discord/__init__.py') as f:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

    if not version:
        raise RuntimeError('version is not set')

    if version.endswith(('a', 'b', 'rc')):
        # append version identifier based on commit count
        suffix = ''
        try:
            import subprocess

            p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                suffix += out.decode('utf-8').strip()
            p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                suffix += '+g' + out.decode('utf-8').strip()
        except Exception:
            pass

        if suffix:
            return f'{version}{suffix}'

        with open('.git_archive_info.txt', encoding='utf-8') as f:
            commit, describe_name = f.read().splitlines()
            if not describe_name:
                # git archive's describe didn't output anything
                return version
            if '%(describe' in describe_name:
                # either git-archive was generated with Git < 2.35 or this is not a git-archive
                return version
            _, _, suffix = describe_name.partition('-')
            if suffix:
                count, _, _ = suffix.partition('-')
            else:
                count = '0'
            version += f'{count}+g{commit}'

    return version


setup(version=derive_version())
