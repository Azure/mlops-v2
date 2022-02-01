# Copyright (c) 2022 Microsoft
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
class LicenseNotAccepted(Exception):
    pass


if "{{ cookiecutter['Do you agree with the license terms for this template? [MIT License]'] }}" == "No":
    raise LicenseNotAccepted("MIT License not accepted - Cookiecutter cancelled. "
                             "See https://github.com/Azure/mlops-v2/blob/main/LICENSE for license details")
