repo_name=$1
project_name=$2
path_to_infrastructure_pipelines=infrastructure/pipelines
path_to_mlops_pipelines=mlops/devops-pipelines

# Resolve the agent queue ID for the hosted "Azure Pipelines" pool. Without
# --queue-id, `az pipelines create` may fail with "Could not queue the build
# because there were validation errors or warnings" on newly-provisioned ADO
# projects where the default queue association has not yet been established.
# Override by exporting AGENT_POOL_NAME before running this script if you use
# a self-hosted pool.
agent_pool_name="${AGENT_POOL_NAME:-Azure Pipelines}"
queue_id=$(az pipelines queue list \
    --project "$project_name" \
    --query "[?name=='$agent_pool_name'].id | [0]" \
    -o tsv)

if [ -z "$queue_id" ]; then
    echo "WARNING: Could not resolve queue ID for agent pool '$agent_pool_name'." >&2
    echo "Pipelines will be created without --queue-id; first run may need to be triggered manually." >&2
fi

cd $repo_name

az pipelines folder create \
    --path $repo_name \
    --project $project_name

az pipelines folder create \
    --path $repo_name/infrastructure \
    --project $project_name

az pipelines folder create \
    --path $repo_name/mlops \
    --project $project_name

mlops_pipeline_files=$(ls $path_to_mlops_pipelines)

for file in $mlops_pipeline_files
do
    az pipelines create \
        --name ${file%.*} \
        --detect true \
        --description "Automatically created pipeline for MLOps $file" \
        --repository $repo_name \
        --branch main \
        --yml-path $path_to_mlops_pipelines/$file \
        --project $project_name \
        --repository-type tfsgit \
        --skip-first-run true \
        --folder-path $repo_name/mlops \
        ${queue_id:+--queue-id $queue_id}
done

infra_pipeline_files=$(ls $path_to_infrastructure_pipelines)

for file in $infra_pipeline_files
do
    az pipelines create \
        --name ${file%.*} \
        --detect true \
        --description "Automatically created pipeline for infra $file" \
        --repository $repo_name \
        --branch main \
        --yml-path $path_to_infrastructure_pipelines/$file \
        --project $project_name \
        --repository-type tfsgit \
        --skip-first-run true \
        --folder-path $repo_name/infrastructure \
        ${queue_id:+--queue-id $queue_id}
done
