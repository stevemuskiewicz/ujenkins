from typing import NamedTuple

from ujenkins.exceptions import JenkinsError

JenkinsVersion = NamedTuple(
    'JenkinsVersion', [('major', int), ('minor', int), ('patch', int)]
)


class System:

    def __init__(self, jenkins):
        self.jenkins = jenkins

    def get_status(self) -> dict:
        """
        Get server status.

        Returns:
            dict: jenkins server details.
        """
        return self.jenkins._request('GET', '/api/json')

    def get_version(self) -> JenkinsVersion:
        """
        Get server version.

        Returns:
            JenkinsVersion: named tuple with minor, major, patch version.
        """
        def callback(response):
            header = response.headers.get('X-Jenkins')
            if not header:
                raise JenkinsError('Header `X-Jenkins` isn`t found in response')

            return JenkinsVersion(*map(int, header.split('.')))

        return self.jenkins._request('GET', '/', callback=callback)

    def is_ready(self) -> bool:
        """
        Determines is server loaded and ready for work.

        Returns:
            bool: ready state.
        """
        def callback(response):
            try:
                status = response.body
                return 'mode' in status
            except JenkinsError:
                return False

        return self.jenkins._request('GET', '/api/json', callback=callback)

    def quiet_down(self) -> None:
        """
        Start server quiet down period, new builds will not be started.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/quietDown')

    def cancel_quiet_down(self) -> None:
        """
        Cancel server quiet down period.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/cancelQuietDown')

    def restart(self) -> None:
        """
        Restart server immediately.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/restart')
