from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.amboss.space/graphql")

query = """
    query Nodes($timeRange: SnapshotTimeRangeEnum) {
  getNetworkMetrics {
    historical_snapshots(timeRange: $timeRange) {
      nodes {
        active
      }
      channels {
        channel_metrics {
          count
          sum
        }
      }
    }
  }
}
    """
def amboss_get_LN_capacity():
    result = client.execute(query=query)
    LN_capacity_in_sats = int(result['data']['getNetworkMetrics']['historical_snapshots']['channels']['channel_metrics']['sum'])
    LN_capacity_in_BTC = int(round(LN_capacity_in_sats / 100000000,0))
    return int(LN_capacity_in_BTC)

if __name__ == "__main__":
    amboss_get_LN_capacity()