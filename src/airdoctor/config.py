from dataclasses import dataclass


@dataclass
class AirDoctorConfig:
    kubeconfig: str = None
    access_token: str = None
    output_dir: str = None


# Not proud of it but not sure how to make it work
global_config = AirDoctorConfig()
