# ibm-spectrum-scale-csi-operator
The [IBM Spectrum Scale Container Storage Interface](https://github.com/IBM/ibm-spectrum-scale-csi) (CSI) project enables container orchestrators, such as Kubernetes and OpenShift, to manage the life-cycle of persistent storage.

This project contains an ansible-based operator to run and manage the deployment of the IBM Spectrum Scale CSI Driver.

# Introduction
This operator installs IBM Spectrum Scale CSI in the cluster, consisting of Attacher and Provisioner StatefulSets, and Driver DaemonSet.

## Details
The standard deployment of this operator consists of one pod for the Attacher and Provisioner each, and a pod on each node the driver is to be used on.

### Configuration
Please refer to the [IBM Documentation](https://www.ibm.com/docs/en/spectrum-scale-csi?topic=220-configurations).

## Installing
Please refer to the [IBM Documentation](https://www.ibm.com/docs/en/spectrum-scale-csi?topic=220-installation).

# Limitations
Please refer to the [IBM Documentation](https://www.ibm.com/docs/en/spectrum-scale-csi?topic=220-limitations).

## Prerequisites
Please refer to the [IBM Documentation](https://www.ibm.com/docs/en/spectrum-scale-csi?topic=installation-performing-pre-tasks).

### Resources Required
Please refer to the [IBM Documentation](https://www.ibm.com/docs/en/spectrum-scale-csi?topic=220-planning).

# PodSecurityPolicy Requirements
This operator does not require any pod  security requirements.

# SecurityContextConstraints Requirements
The operator maintains the Security Context Constraints, removing the required restraints when the operator is uninstalled.
