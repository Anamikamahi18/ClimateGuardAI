function RiskCard({
  title,
  value,
  confidence,
}) {
  return (
    <div className="risk-card">
      <h3>{title}</h3>

      <h2>{value}</h2>

      {confidence !== undefined && (
        <p>
          Confidence:
          {" "}
          {confidence}%
        </p>
      )}
    </div>
  );
}

export default RiskCard;
