import React, { useEffect, useState } from "react";

function Test() {
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetch("/members")
      .then((res) => res.json()) // Corrected syntax: semicolon replaced with a comma
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  return <div>Test</div>;
}

export default Test;
