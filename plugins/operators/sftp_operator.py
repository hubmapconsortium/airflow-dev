import os
import re
from pathlib import Path

from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.sftp_operator import SFTPOperator
from airflow.exceptions import AirflowException


class HiveSFTPOperator(SFTPOperator):
    def __init__(self, job_id=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.job_id = job_id

    def execute(self, context):
        try:
            if self.ssh_conn_id:
                if self.ssh_hook and isinstance(self.ssh_hook, SSHHook):
                    self.log.info("ssh_conn_id is ignored when ssh_hook is provided.")
                else:
                    self.log.info("ssh_hook is not provided or invalid. " +
                                  "Trying ssh_conn_id to create SSHHook.")
                    self.ssh_hook = SSHHook(ssh_conn_id=self.ssh_conn_id)

            if not self.ssh_hook:
                raise AirflowException("Cannot operate without ssh_hook or ssh_conn_id.")

            if self.remote_host is not None:
                self.log.info("remote_host is provided explicitly. " +
                              "It will replace the remote_host which was defined " +
                              "in ssh_hook or predefined in connection of ssh_conn_id.")
                self.ssh_hook.remote_host = self.remote_host

            slurm_job_output = context['task_instance'].xcom_pull(task_ids='submit_slurm_job')
            slurm_job_output = slurm_job_output.decode("utf-8")

            regex = re.search('([0-9]+)', slurm_job_output)
            if regex.group(0):
                self.job_id = regex.group(0)
            else:
                raise AirflowException("Error while parsing SLURM output files. No job id present in XCom data.")

            file_list = slurm_job_output.split("[HubFS]")[1:]  # Get file list after the field separator.
            file_list = file_list[0][:-1].replace("\n", "[HubFS]").split("[HubFS]")  # Remove rightmost new line char

            # define the name of the directory to be created
            current_path = os.getenv('AIRFLOW_HOME')
            new_dir_path = current_path + "/slurm_output_files/" + self.job_id
            try:
                Path(new_dir_path).mkdir(parents=True, exist_ok=True)
            except OSError:
                self.log.error("Creation of the directory %s failed" % new_dir_path)
            else:
                self.log.info("Successfully created the directory %s " % new_dir_path)

            with self.ssh_hook.get_conn() as ssh_client:
                sftp_client = ssh_client.open_sftp()

                for remote_file_path in file_list:
                    remote_file_path = remote_file_path.strip()
                    self.log.info('source file_path: %s', remote_file_path)

                    remote_path, file = os.path.split(remote_file_path)
                    self.log.info('path: %s', remote_path)
                    self.log.info('file: %s', file)

                    local_filepath = new_dir_path + "/" + file
                    self.local_filepath = local_filepath
                    self.log.info('destination (local) file_path: %s', local_filepath)

                    sftp_client.get(remote_file_path, local_filepath)
        except Exception as e:
            raise AirflowException("Error while transferring.")

        return self.local_filepath
