function DriverTable({
  title,
  drivers,
}) {

  return (

    <div
      className="table-container"
    >

      <h3>{title}</h3>

      <table>

        <thead>
          <tr>
            <th>Feature</th>
            <th>Value</th>
            <th>Impact</th>
            <th>Strength</th>
          </tr>
        </thead>

        <tbody>

          {drivers.map(
            (driver) => (

              <tr
                key={
                  driver.feature
                }
              >

                <td>
                  {
                    driver.display_name
                  }
                </td>

                <td>
                  {
                    driver.feature_value
                  }
                </td>

                <td>
                  {
                    driver.impact
                  }
                </td>

                <td>
                  {
                    driver.strength
                  }
                </td>

              </tr>
            )
          )}

        </tbody>

      </table>

    </div>
  );
}

export default DriverTable;
